from langchain.document_loaders import PyMuPDFLoader
from models.files import File

from .common import process_file


def process_odt(file: File, enable_summarization, brain_id, user_openai_api_key):
    return process_file(
        file=file,
        loader_class=PyMuPDFLoader,
        enable_summarization=enable_summarization,
        brain_id=brain_id,
        user_openai_api_key=user_openai_api_key,
    )
