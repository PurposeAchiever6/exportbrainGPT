from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from routes.authorizations.types import RoleEnum


class BrainEntity(BaseModel):
    brain_id: UUID
    name: str
    description: Optional[str]
    temperature: Optional[float]
    model: Optional[str]
    max_tokens: Optional[int]
    openai_api_key: Optional[str]
    status: Optional[str]
    prompt_id: Optional[UUID]
    extraversion: Optional[int]
    neuroticism: Optional[int]
    conscientiousness: Optional[int]

    @property
    def id(self) -> UUID:
        return self.brain_id

    def dict(self, **kwargs):
        data = super().dict(
            **kwargs,
        )
        data["id"] = self.id
        return data


class MinimalBrainEntity(BaseModel):
    id: UUID
    name: str
    rights: RoleEnum
