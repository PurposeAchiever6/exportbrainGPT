from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from models.databases.repository import Repository


class Vector_qdrant():
    def __init__(self, qdrant_client: QdrantClient, encoder_model: str = 'all-MiniLM-L6-v2'):
        self.db: QdrantClient = qdrant_client
        self.encoder = SentenceTransformer(encoder_model)

    def get_payloads_data_sha1(self, data_sha1):
        response = self.db.scroll(
            collection_name="vectors",
            scroll_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="data_sha1",
                        match=models.MatchValue(value=data_sha1),
                    )
                ]
            ),
        )
        return response
    
    def delete_vectors_from_brain(self, brain_id, data_sha1):
        response = self.db.delete(
            collection_name="vectors",
                points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="data_sha1",
                            match=models.MatchValue(value=data_sha1),
                        ),
                        models.FieldCondition(
                            key="brain_id",
                            match=models.MatchValue(value=str(brain_id)),
                        ),
                    ],
                )
            ),
        )
        return response
    
    def delete_all_vectors_from_brain(self, brain_id):
        response = self.db.delete(
            collection_name="vectors",
                points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="brain_id",
                            match=models.MatchValue(value=str(brain_id)),
                        ),
                    ],
                )
            ),
        )
        return response
    
    def get_nearest_brain_list(self, query:str, limit:int=5):
        respond = self.db.search_groups(
            collection_name="vectors",
            query_vector=self.encoder.encode(query).tolist(),
            group_by="brain_id",
            with_payload=["brain_id"],
            limit=limit
        )
        brain_id_scores = [{"brain_id": group.hits[0].payload['brain_id'], "score": group.hits[0].score} for group in respond.groups]
        return brain_id_scores
    