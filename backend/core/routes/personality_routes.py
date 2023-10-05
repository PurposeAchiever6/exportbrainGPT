import json
from dotenv import load_dotenv
from auth import AuthBearer, get_current_user
from fastapi import APIRouter, Depends
from repository.personality.personality_question import generate_question_all
from repository.personality.personality import personality

personality_router = APIRouter()

# get personality questions
@personality_router.get("/personality/question", dependencies=[Depends(AuthBearer())], tags=["Personality"])
async def get_personality_questions(question_number:int = 1):
    """
    Generate personality questions for testing expert's personality.

    - Returns a list of questions.

    - Example:

    This endpoint generates questions associated with the all kinds of traits. It returns list of questions
    """
    return generate_question_all(question_number)


# get personality from test results
@personality_router.post("/personality/", dependencies=[Depends(AuthBearer())], tags=["Personality"])
async def get_personality(results):
    return personality(results)