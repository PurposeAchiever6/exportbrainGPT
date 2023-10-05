from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from models.brain_entity import BrainEntity


class Repository(ABC):
    @abstractmethod
    def get_user_brains(self, user_id: str) -> list[BrainEntity]:
        pass

    @abstractmethod
    def get_brain_for_user(self, user_id: str):
        pass

    @abstractmethod
    def delete_brain_user_by_id(self, user_id: str, brain_id: str):
        pass

    @abstractmethod
    def delete_brain_vector(self, brain_id: str):
        pass

    @abstractmethod
    def delete_brain_user(self, brain_id: str):
        pass

    @abstractmethod
    def delete_brain(self, brain_id: str):
        pass

    @abstractmethod
    def create_brain(self, brain: str):
        pass

    @abstractmethod
    def create_brain_user(
        self, user_id: UUID, brain_id: UUID, rights: str, default_brain: bool
    ):
        pass

    @abstractmethod
    def create_brain_vector(self, brain_id: UUID, vector_id: UUID, file_sha1: str):
        pass

    @abstractmethod
    def get_vector_ids_from_file_sha1(self, file_sha1: str):
        pass

    @abstractmethod
    def get_brain_vector_ids(self, brain_id: UUID):
        pass

    @abstractmethod
    def delete_file_from_brain(self, brain_id: UUID, file_name: str):
        pass

    @abstractmethod
    def get_default_user_brain_id(self, user_id: UUID) -> UUID:
        pass

    @abstractmethod
    def get_brain_by_id(self, brain_id: UUID):
        pass

    @abstractmethod
    def create_user(self, user_id: UUID, user_email: str, date: datetime):
        pass

    @abstractmethod
    def get_user_request_stats(self, user_id: UUID):
        pass

    @abstractmethod
    def fetch_user_requests_count(self, user_id: UUID, date: str):
        pass

    @abstractmethod
    def update_user_request_count(self, date: str):
        pass

    @abstractmethod
    def get_user_email(self, user_id: UUID):
        pass

    @abstractmethod
    def set_file_vectors_ids(self, file_sha1: str):
        pass

    @abstractmethod
    def get_brain_vectors_by_brain_id_and_file_sha1(
        self, brain_id: UUID, file_sha1: str
    ):
        pass

    @abstractmethod
    def get_brain_data_by_brain_id_and_data_sha1(
        self, brain_id: UUID, data_sha1: str
    ):
        pass

    @abstractmethod
    def create_subscription_invitation(
        self, brain_id: UUID, user_email: str, rights: str
    ):
        pass

    @abstractmethod
    def update_subscription_invitation(
        self, brain_id: UUID, user_email: str, rights: str
    ):
        pass

    @abstractmethod
    def get_subscription_invitations_by_brain_id_and_email(
        self, brain_id: UUID, user_email: str
    ):
        pass

    @abstractmethod
    def create_api_key(self, new_key_id: UUID, new_api_key: str, user_id: UUID):
        pass

    @abstractmethod
    def delete_api_key(self, key_id: UUID, user_id: UUID):
        pass

    @abstractmethod
    def get_active_api_key(self, api_key: UUID):
        pass

    @abstractmethod
    def get_user_id_by_api_key(self, api_key: UUID):
        pass

    @abstractmethod
    def get_user_stats(self, user_email: str, date: datetime):
        pass

    @abstractmethod
    def create_chat(self, new_chat):
        pass

    @abstractmethod
    def get_chat_by_id(self, chat_id: str):
        pass

    @abstractmethod
    def get_chat_history(self, chat_id: str):
        pass

    @abstractmethod
    def get_user_chats(self, user_id: str):
        pass

    @abstractmethod
    def update_chat_history(self, chat_id: str, user_message: str, assistant: str):
        pass

    @abstractmethod
    def update_chat(self, chat_id: UUID, updates):
        pass

    @abstractmethod
    def update_message_by_id(self, message_id: UUID, updates):
        pass

    @abstractmethod
    def get_chat_details(self, chat_id: UUID):
        pass

    @abstractmethod
    def delete_chat(self, chat_id: UUID):
        pass

    @abstractmethod
    def delete_chat_history(self, chat_id: UUID):
        pass

    @abstractmethod
    def get_vectors_by_file_name(self, file_name: str):
        pass

    @abstractmethod
    def similarity_search(
        self, query_embedding, table: str, top_k: int, threshold: float
    ):
        pass

    @abstractmethod
    def update_summary(self, document_id: UUID, summary_id: int):
        pass

    @abstractmethod
    def get_vectors_by_batch(self, batch_id: UUID):
        pass

    @abstractmethod
    def get_vectors_in_batch(self, batch_ids):
        pass

    @abstractmethod
    def get_vectors_by_file_sha1(self, file_sha1):
        pass

    @abstractmethod
    def create_prompt(self, new_prompt):
        pass

    @abstractmethod
    def get_prompt_by_id(self, prompt_id: UUID):
        pass

    @abstractmethod
    def delete_prompt_by_id(self, prompt_id: UUID):
        pass

    @abstractmethod
    def update_prompt_by_id(self, prompt_id: UUID, updates):
        pass

    @abstractmethod
    def get_public_prompts(self):
        pass

    # Qdrant
    @abstractmethod
    def get_payloads_data_sha1(self, data_sha1:str):
        pass