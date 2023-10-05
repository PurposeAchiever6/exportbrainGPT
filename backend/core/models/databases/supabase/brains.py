from typing import Optional
from uuid import UUID

from logger import get_logger
from models.brain_entity import BrainEntity, MinimalBrainEntity
from models.databases.repository import Repository
from pydantic import BaseModel

logger = get_logger(__name__)


class CreateBrainProperties(BaseModel):
    name: Optional[str] = "Default brain"
    description: Optional[str] = "This is a description"
    status: Optional[str] = "private"
    model: Optional[str] = "gpt-3.5-turbo-0613"
    temperature: Optional[float] = 0.0
    max_tokens: Optional[int] = 256
    openai_api_key: Optional[str] = None
    prompt_id: Optional[UUID] = None
    linkedin: Optional[str] = None
    extraversion: Optional[int] = None
    neuroticism: Optional[int] = None
    conscientiousness: Optional[int] = None

    def dict(self, *args, **kwargs):
        brain_dict = super().dict(*args, **kwargs)
        if brain_dict.get("prompt_id"):
            brain_dict["prompt_id"] = str(brain_dict.get("prompt_id"))
        return brain_dict


class BrainUpdatableProperties(BaseModel):
    name: Optional[str]
    description: Optional[str]
    temperature: Optional[float]
    model: Optional[str]
    max_tokens: Optional[int]
    openai_api_key: Optional[str]
    status: Optional[str]
    prompt_id: Optional[UUID]

    def dict(self, *args, **kwargs):
        brain_dict = super().dict(*args, **kwargs)
        if brain_dict.get("prompt_id"):
            brain_dict["prompt_id"] = str(brain_dict.get("prompt_id"))
        return brain_dict


class Brain(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    def create_brain(self, brain: CreateBrainProperties):
        response = (self.db.table("brains").insert(brain.dict())).execute()
        return BrainEntity(**response.data[0])

    def get_user_brains(self, user_id) -> list[MinimalBrainEntity]:
        response = (
            self.db.from_("brains_users")
            .select("id:brain_id, rights, brains (id: brain_id, name)")
            .filter("user_id", "eq", user_id)
            .execute()
        )
        user_brains: list[MinimalBrainEntity] = []
        for item in response.data:
            user_brains.append(
                MinimalBrainEntity(
                    id=item["brains"]["id"],
                    name=item["brains"]["name"],
                    rights=item["rights"],
                )
            )
            user_brains[-1].rights = item["rights"]
        return user_brains

    def get_all_brains(self) -> list[MinimalBrainEntity]:
        response = (
            self.db.from_("brains_users")
            .select("id:brain_id, rights, brains (id: brain_id, name)")
            .execute()
        )
        user_brains: list[MinimalBrainEntity] = []
        for item in response.data:
            user_brains.append(
                MinimalBrainEntity(
                    id=item["brains"]["id"],
                    name=item["brains"]["name"],
                    rights=item["rights"],
                )
            )
            user_brains[-1].rights = item["rights"]
        return user_brains

    def get_brain_for_user(self, user_id, brain_id) -> MinimalBrainEntity | None:
        response = (
            self.db.from_("brains_users")
            .select("id:brain_id, rights, brains (id: brain_id, name)")
            .filter("user_id", "eq", user_id)
            .filter("brain_id", "eq", brain_id)
            .execute()
        )
        if len(response.data) == 0:
            return None
        brain_data = response.data[0]

        return MinimalBrainEntity(
            id=brain_data["brains"]["id"],
            name=brain_data["brains"]["name"],
            rights=brain_data["rights"],
        )

    def get_brain_details(self, brain_id):
        response = (
            self.db.from_("brains")
            .select("id:brain_id, name, *")
            .filter("brain_id", "eq", brain_id)
            .execute()
        )
        return response.data

    def delete_brain_user_by_id(self, user_id, brain_id):
        results = (
            self.db.table("brains_users")
            .select("*")
            .match({"brain_id": brain_id, "user_id": user_id, "rights": "Owner"})
            .execute()
        )
        return results

    def delete_brain_vector(self, brain_id: str):
        results = (
            self.db.table("brains_vectors")
            .delete()
            .match({"brain_id": brain_id})
            .execute()
        )

        return results

    def delete_brain_user(self, brain_id: str):
        results = (
            self.db.table("brains_users")
            .delete()
            .match({"brain_id": brain_id})
            .execute()
        )

        return results

    def delete_brain(self, brain_id: str):
        results = (
            self.db.table("brains").delete().match({"brain_id": brain_id}).execute()
        )

        return results

    def create_brain_user(self, user_id: UUID, brain_id, rights, default_brain: bool):
        response = (
            self.db.table("brains_users")
            .insert(
                {
                    "brain_id": str(brain_id),
                    "user_id": str(user_id),
                    "rights": rights,
                    "default_brain": default_brain,
                }
            )
            .execute()
        )

        return response

    def create_brain_vector(self, brain_id, vector_id, file_sha1):
        response = (
            self.db.table("brains_vectors")
            .insert(
                {
                    "brain_id": str(brain_id),
                    "vector_id": str(vector_id),
                    "file_sha1": file_sha1,
                }
            )
            .execute()
        )
        return response.data
    
    def create_brain_data(self, brain_id, data_sha1, metadata=None):
        response = (
            self.db.table("brains_data")
            .insert(
                {
                    "brain_id": str(brain_id),
                    "data_sha1": data_sha1,
                    "metadata": metadata
                }
            )
            .execute()
        )
        return response.data

    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        # move to vectors class
        vectorsResponse = (
            self.db.table("vectors")
            .select("id")
            .filter("metadata->>file_sha1", "eq", file_sha1)
            .execute()
        )
        return vectorsResponse.data

    def update_brain_by_id(
        self, brain_id: UUID, brain: BrainUpdatableProperties
    ) -> BrainEntity | None:
        update_brain_response = (
            self.db.table("brains")
            .update(brain.dict(exclude_unset=True))
            .match({"brain_id": brain_id})
            .execute()
        ).data

        if len(update_brain_response) == 0:
            return None

        return BrainEntity(**update_brain_response[0])

    def get_brain_vector_ids(self, brain_id):
        """
        Retrieve unique brain data (i.e. uploaded files and crawled websites).
        """

        response = (
            self.db.from_("brains_vectors")
            .select("vector_id")
            .filter("brain_id", "eq", brain_id)
            .execute()
        )

        vector_ids = [item["vector_id"] for item in response.data]

        if len(vector_ids) == 0:
            return []

        return vector_ids

    def delete_file_from_brain(self, brain_id, file_name: str):
        # First, get the vector_ids associated with the file_name
        vector_response = (
            self.db.table("vectors")
            .select("id")
            .filter("metadata->>file_name", "eq", file_name)
            .execute()
        )
        vector_ids = [item["id"] for item in vector_response.data]

        # For each vector_id, delete the corresponding entry from the 'brains_vectors' table
        for vector_id in vector_ids:
            self.db.table("brains_vectors").delete().filter(
                "vector_id", "eq", vector_id
            ).filter("brain_id", "eq", brain_id).execute()

            # Check if the vector is still associated with any other brains
            associated_brains_response = (
                self.db.table("brains_vectors")
                .select("brain_id")
                .filter("vector_id", "eq", vector_id)
                .execute()
            )
            associated_brains = [
                item["brain_id"] for item in associated_brains_response.data
            ]

            # If the vector is not associated with any other brains, delete it from 'vectors' table
            if not associated_brains:
                self.db.table("vectors").delete().filter(
                    "id", "eq", vector_id
                ).execute()

        return {"message": f"File {file_name} in brain {brain_id} has been deleted."}

    def delete_data_from_brain(self, brain_id, data_sha1):
        # First, get the vector_ids associated with the file_name
        self.db.table("brains_data").delete().filter(
            "brain_id", "eq", brain_id
        ).filter(
            "data_sha1", "eq", data_sha1
        ).execute()

        return {"message": f"Data {data_sha1} in brain {brain_id} has been deleted."}
        # vector_response = (
        #     self.db.table("brains_data")
        #     .select("id")
        #     .filter("metadata->>file_name", "eq", file_name)
        #     .execute()
        # )
        # vector_ids = [item["id"] for item in vector_response.data]

        # # For each vector_id, delete the corresponding entry from the 'brains_vectors' table
        # for vector_id in vector_ids:
        #     self.db.table("brains_vectors").delete().filter(
        #         "vector_id", "eq", vector_id
        #     ).filter("brain_id", "eq", brain_id).execute()

        #     # Check if the vector is still associated with any other brains
        #     associated_brains_response = (
        #         self.db.table("brains_vectors")
        #         .select("brain_id")
        #         .filter("vector_id", "eq", vector_id)
        #         .execute()
        #     )
        #     associated_brains = [
        #         item["brain_id"] for item in associated_brains_response.data
        #     ]

        #     # If the vector is not associated with any other brains, delete it from 'vectors' table
        #     if not associated_brains:
        #         self.db.table("vectors").delete().filter(
        #             "id", "eq", vector_id
        #         ).execute()

        # return {"message": f"File {file_name} in brain {brain_id} has been deleted."}

    def get_default_user_brain_id(self, user_id: UUID) -> UUID | None:
        response = (
            (
                self.db.from_("brains_users")
                .select("brain_id")
                .filter("user_id", "eq", user_id)
                .filter("default_brain", "eq", True)
                .execute()
            )
        ).data
        if len(response) == 0:
            return None
        return UUID(response[0].get("brain_id"))

    def get_brain_by_id(self, brain_id: UUID) -> BrainEntity | None:
        response = (
            self.db.from_("brains")
            .select("id:brain_id, name, *")
            .filter("brain_id", "eq", brain_id)
            .execute()
        ).data

        if len(response) == 0:
            return None

        return BrainEntity(**response[0])
