# from typing import List

# from models.chat import ChatHistory
# from models.settings import get_supabase_db, get_qdrant_db # For type hinting


# def get_nearest_brains(query: str, limit:int) -> List[str]:
#     # settings = DatabaseSettings()
#     # encoder = SentenceTransformer('all-MiniLM-L6-v2')
#     qdrant_client = get_qdrant_db
#     groups = qdrant_client.search_groups(
#         collection_name="vectors",
#         query_vector=encoder.encode(query).tolist(),
#         group_by="data_sha1",
#         with_payload=["data_sha1"],
#         limit=5
#     )
#     data_sha1_list = [group.hits[0].payload['data_sha1'] for group in groups]
    # supabase_db = get_supabase_db()
    # brain_list = 
    # supabase_db = get_supabase_db()
    # history: List[ChatHistory] = supabase_db.get_chat_history(chat_id).data
    # if history is None:
    #     return []
    # else:
    #     return [
    #         ChatHistory(message)  # pyright: ignore reportPrivateUsage=none
    #         for message in history
    #     ]
