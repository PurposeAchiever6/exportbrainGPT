from typing import Any, List, Optional
from pydantic import BaseModel

class TestResult(BaseModel):
    trait: Optional[str] = "Extraversion"
    positive: bool = True,
    question: Optional[str] = ""
    answer: Optional[int] = 0

# class TestResultList(BaseModel):
#     results: List[TestResult] = []