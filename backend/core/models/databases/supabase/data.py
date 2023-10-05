from models.databases.repository import Repository


class Data(Repository):
    def __init__(self, supabase_client):
        self.db = supabase_client

    # def set_file_vectors_ids(self, file_sha1):
    #     response = (
    #         self.db.table("vectors")
    #         .select("id")
    #         .filter("metadata->>file_sha1", "eq", file_sha1)
    #         .execute()
    #     )
    #     return response.data

    def get_brain_data_by_brain_id_and_data_sha1(self, brain_id, data_sha1):
        # Check if file exists in that brain
        response = (
            self.db.table("brains_data")
            .select("brain_id, data_sha1")
            .filter("brain_id", "eq", brain_id)
            .filter("data_sha1", "eq", data_sha1)
            .execute()
        )

        return response
