from pydantic import BaseModel
from typing import List

class CandidateIn(BaseModel):
    name: str
    age: int
    city: str
    school: str
    gpa: float
    achievements: str
    essay: str
    motivation: str
