import os
from dotenv import load_dotenv
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

load_dotenv()
qdrant_location = os.getenv("QDRANT_LOCATION")
qdrant_port = os.getenv("QDRANT_PORT")
qdrant = QdrantClient(location=qdrant_location, port=qdrant_port)
encoder = SentenceTransformer('all-MiniLM-L6-v2') 

try:
    qdrant.recreate_collection(
        collection_name="vectors",
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(), # Vector size is defined by used model
            distance=models.Distance.COSINE
        )
    )
except Exception as e:
    print(e)
