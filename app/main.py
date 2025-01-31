from fastapi import FastAPI

from llm.models import RawAnswer

from .agent import ITMOSearchAgent
from .models import RequestModel, ResponseModel

app = FastAPI()
agent = ITMOSearchAgent()


@app.post("/api/request", response_model=ResponseModel)
async def handle_request(request: RequestModel):
    query = request.query
    answer = await agent.get_answer(query)
    if isinstance(answer, RawAnswer):
        return ResponseModel(
            id=request.id,
            answer=answer.answer,
            reasoning="Ответ бы сгенерирован моделью gpt-4o" + "\n" + answer.reasoning,
            sources=["Знания gpt-4o"],
        )
    else:
        return ResponseModel(
            id=request.id,
            answer=answer.answer if agent.choose_answer else None,
            reasoning=answer.reasoning,
            sources=answer.sources,
        )
