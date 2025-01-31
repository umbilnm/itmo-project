from typing import List, Optional

from pydantic import BaseModel


class RawAnswer(BaseModel):
    reasoning: str
    answer: Optional[int] = None


class ChosenPages(BaseModel):
    nums: List[int]


class AgentAnswer(BaseModel):
    question: str
    reasoning: str
    can_answer: bool
    tools: Optional[List[int]] = None


class AnswerWithContext(BaseModel):
    answer: int
    reasoning: str
    sources: List[str]
