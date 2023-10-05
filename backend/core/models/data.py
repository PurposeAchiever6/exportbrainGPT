import os
import tempfile
from typing import Any, Optional
import uuid
from uuid import UUID

from fastapi import UploadFile
from langchain.text_splitter import RecursiveCharacterTextSplitter
from logger import get_logger
from models.brains import Brain
from models.databases.supabase.supabase import SupabaseDB
from models.databases.qdrant.qdrant import QdrantDB
from models.settings import get_supabase_db, get_qdrant_db
from pydantic import BaseModel
from utils.file import compute_sha1_from_file, compute_sha1_from_string

logger = get_logger(__name__)


class Data(BaseModel):
    id: Optional[UUID] = None
    data: Optional[str]
    data_name: Optional[str] = ""
    data_size: Optional[int] = None
    data_sha1: Optional[str] = ""
    vectors_ids: Optional[list] = []
    payloads: Optional[list] = []
    # file_extension: Optional[str] = ""
    content: Optional[Any] = None
    chunk_size: int = 500
    chunk_overlap: int = 0
    documents: Optional[Any] = None

    @property
    def supabase_db(self) -> SupabaseDB:
        return get_supabase_db()

    @property
    def qdrant_db(self) -> QdrantDB:
        return get_qdrant_db()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if self.data:
            self.data_size = len(self.data)  # pyright: ignore reportPrivateUsage=none
            # self.file_extension = os.path.splitext(
            #     self.file.filename  # pyright: ignore reportPrivateUsage=none
            # )[-1].lower()

    async def compute_data_sha1(self):
        """
        Compute the sha1 of the data
        """
        self.data_sha1 = compute_sha1_from_string(self.data)

    def compute_documents(self):
        """
        Compute the documents from the data
        """
        logger.info(f"Computing documents from data")

        # documents = []
        # with tempfile.NamedTemporaryFile(
        #     delete=False,
        #     suffix=self.file.filename,  # pyright: ignore reportPrivateUsage=none
        # ) as tmp_file:
        #     tmp_file.write(self.content)  # pyright: ignore reportPrivateUsage=none
        #     tmp_file.flush()
        #     loader = loader_class(tmp_file.name)
        #     documents = loader.load()

        #     print("documents", documents)

        # os.remove(tmp_file.name)

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        self.documents = text_splitter.split_text(self.data)

        print(self.documents)

    def set_file_vectors_ids(self):
        """
        Set the vectors_ids property with the ids of the vectors
        that are associated with the file in the vectors table
        """
        self.vectors_ids = self.supabase_db.get_vectors_by_file_sha1(
            self.data_sha1
        )
    
    def set_payloads(self):
        """
        Set the vectors_ids property with the ids of the vectors
        that are associated with the file in the vectors table
        """
        self.payloads = self.qdrant_db.get_payloads_data_sha1(
            self.data_sha1
        )[0]

    def data_already_exists(self):
        """
        Check if data already exists in vectors colloection
        """
        self.set_payloads()

        print("data_sha1", self.data_sha1)
        print("payloads", self.payloads)
        print(
            "len(payloads)",
            len(self.payloads),  # pyright: ignore reportPrivateUsage=none
        )

        # if the data does not exist in vectors then no need to go check in brains_vectors
        if len(self.payloads) == 0:  # pyright: ignore reportPrivateUsage=none
            return False

        return True

    # def file_already_exists_qdrant(self):
    #     """
    #     Check if file already exists in vectors table
    #     """
    #     self.set_file_vectors_ids()

    #     print("file_sha1", self.file_sha1)
    #     print("vectors_ids", self.vectors_ids)
    #     print(
    #         "len(vectors_ids)",
    #         len(self.vectors_ids),  # pyright: ignore reportPrivateUsage=none
    #     )

    #     # if the file does not exist in vectors then no need to go check in brains_vectors
    #     if len(self.vectors_ids) == 0:  # pyright: ignore reportPrivateUsage=none
    #         return False

    #     return True

    def data_already_exists_in_brain(self, brain_id):
        """
        Check if data already exists in a brain

        Args:
            brain_id (str): Brain id
        """
        response = self.supabase_db.get_brain_data_by_brain_id_and_data_sha1(
            brain_id, self.data_sha1
        )

        print("response.data", response.data)
        if len(response.data) == 0:
            return False

        return True

    def data_is_empty(self):
        """
        Check if file is empty by checking if the file pointer is at the beginning of the file
        """
        return (
            len(self.data) < 1  # pyright: ignore reportPrivateUsage=none
        )

    def link_data_to_brain(self, brain: Brain):
        self.id = uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name=self.data_sha1)
        brain.create_brain_data(data_sha1=self.data_sha1)
        print(f"Successfully linked file {self.data_sha1} to brain {brain.id}")

    def upload_records_qdrant(self, records):
        self.qdrant_db.upload_records(records)