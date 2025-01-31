from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class RawAnswer(BaseModel):
    reasoning: str
    answer: Optional[int] = None


class ChosenPages(BaseModel):
    nums: List[int]


class AgentAnswer(BaseModel):
    question: str = Field(description="Вопрос пользователя")
    reasoning: str = Field(
        description="Пояснение, почему могу или не могу ответить на вопрос"
    )
    choose_answer: bool = Field(
        description="Если вопрос содержит пронумерованные варианты ответов, верни True, иначе False"
    )
    confidence_level: bool = Field(
        description="Напиши уровень уверенности в том, что можешь ответить на вопрос"
    )


class AnswerWithContext(BaseModel):
    answer: int
    reasoning: str
    sources: List[str]
