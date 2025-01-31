import os

from dotenv import load_dotenv
from openai import AsyncOpenAI
from yaml import safe_load

from app.utils import log_llm_response

from .models import AgentAnswer, AnswerWithContext, RawAnswer

load_dotenv()

prompts = safe_load(open("llm/prompts.yaml"))
client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0.0,
)


async def raw_answer(query: str) -> RawAnswer:
    response = await client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL"),
        response_format=RawAnswer,
        messages=[
            {"role": "system", "content": prompts["raw_answer"].format(question=query)},
        ],
    )
    result = response.choices[0].message.parsed
    log_llm_response("raw_answer", query, result.model_dump())
    return result


async def agent_plan(question: str) -> AgentAnswer:
    response = await client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL"),
        response_format=AgentAnswer,
        messages=[
            {
                "role": "system",
                "content": prompts["agent_prompt"].format(question=question),
            }
        ],
    )
    result = response.choices[0].message.parsed
    log_llm_response("agent_plan", question, result.model_dump())
    return result


async def answer_with_context(query: str, context: str) -> str:
    response = await client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL"),
        response_format=AnswerWithContext,
        messages=[
            {
                "role": "system",
                "content": prompts["answer_with_context"].format(
                    question=query, context=context
                ),
            },
        ],
    )
    result = response.choices[0].message.parsed
    log_llm_response("answer_with_context", query, result.model_dump())
    return result
