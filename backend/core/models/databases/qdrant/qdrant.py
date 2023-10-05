from logger import get_logger
from sentence_transformers import SentenceTransformer
from models.databases.qdrant import (
    Vector_qdrant, Data
)

logger = get_logger(__name__)


class QdrantDB(
    Vector_qdrant, Data
):
    def __init__(self, qdrant_client, encoder_model: str = 'all-MiniLM-L6-v2'):
        self.db = qdrant_client
        self.encoder = SentenceTransformer(encoder_model)
        Vector_qdrant.__init__(self, qdrant_client, encoder_model=encoder_model)
        Data.__init__(self, qdrant_client)

