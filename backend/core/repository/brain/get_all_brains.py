from uuid import UUID

from models.brain_entity import BrainEntity
from models.settings import get_supabase_db

def get_all_brains() -> list[BrainEntity]:
    supabase_db = get_supabase_db()
    results = supabase_db.get_all_brains()

    return results
