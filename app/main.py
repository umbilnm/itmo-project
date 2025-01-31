import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException

from llm.models import RawAnswer

from .agent import ITMOSearchAgent
from .models import RequestModel, ResponseModel

logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(logs_dir / "app.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)

app = FastAPI()
agent = ITMOSearchAgent()


@app.post("/api/request", response_model=ResponseModel)
async def handle_request(request: RequestModel):
    query = request.query
    logger.info(f"Received request ID: {request.id} with query: {query}")

    try:
        logger.info(f"Processing query: {request.query}")
        answer = await agent.get_answer(query)
        reasoning = (
            "Ответ бы сгенерирован моделью gpt-4o-mini" + "\n" + answer.reasoning
        )

        if isinstance(answer, RawAnswer):

            response = ResponseModel(
                id=request.id,
                answer=answer.answer,
                reasoning=reasoning,
                sources=["Знания gpt-4o-mini"],
            )
        else:
            response = ResponseModel(
                id=request.id,
                answer=answer.answer if agent.choose_answer is True else None,
                reasoning=reasoning,
                sources=answer.sources,
            )

        logger.info(
            f"Request ID: {request.id} \n Generated answer: {answer.answer} \n Reasoning: {answer.reasoning}"
        )
        return response

    except Exception as e:
        logger.error(f"Error processing request ID {request.id}: {str(e)}")
        error_msg = f"Error processing request: {str(e)}"
        raise HTTPException(status_code=500, detail=error_msg)
