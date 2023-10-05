from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer

# client = QdrantClient(path="/root/hongyu/customersupportgpt/quivr_project/backend/core/db")
qdrant = QdrantClient("localhost", port=6333)
encoder = SentenceTransformer('all-MiniLM-L6-v2') 

try:
    qdrant.create_collection(
        collection_name="Linkedin_profile",
        vectors_config=models.VectorParams(
            size=encoder.get_sentence_embedding_dimension(), # Vector size is defined by used model
            distance=models.Distance.COSINE
        )
    )
except:
    pass

with open('/root/hongyu/customersupportgpt/quivr_project/backend/core/tests/test_files/test_linedin_information_sample.txt', 'r') as f:
    linkedin_data = f.read()

record = models.Record(
			id=0,
			vector=encoder.encode(linkedin_data).tolist(),
			payload={"data": linkedin_data}
		)

qdrant.upload_records(
	collection_name="Linkedin_profile",
	records=[
		record
	]
)
# qdrant.upload_records(
# 	collection_name="Linkedin_profile",
# 	records=[
# 		models.Record(
# 			id=0,
# 			vector=encoder.encode(linkedin_data).tolist(),
# 			payload=linkedin_data
# 		)
# 	]
# )

# vector = encoder.encode(linkedin_data)
