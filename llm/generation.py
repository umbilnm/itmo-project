import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from yaml import safe_load

from .models import AgentAnswer, AnswerWithContext, ChosenPages, RawAnswer

load_dotenv()

prompts = safe_load(open("llm/prompts.yaml"))
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL")
)


def raw_answer(query: str) -> RawAnswer:
    response = client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL"),
        response_format=RawAnswer,
        messages=[
            {"role": "system", "content": prompts["raw_answer"].format(question=query)},
        ],
    )
    return response.choices[0].message.parsed


def validate_pages(links: str) -> ChosenPages:
    response = client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL"),
        response_format=ChosenPages,
        messages=[
            {"role": "system", "content": prompts["validate_prompt"]},
            {"role": "user", "content": links},
        ],
    )
    return response.choices[0].message.parsed


def summarize(text: str, question: str) -> str:
    response = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": prompts["find_answer_prompt"].format(question=question),
            },
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content


def agent_plan(question: str) -> AgentAnswer:
    response = client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL"),
        response_format=AgentAnswer,
        messages=[
            {
                "role": "system",
                "content": prompts["agent_prompt"].format(question=question),
            }
        ],
    )
    return response.choices[0].message.parsed


def answer_with_context(query: str, context: str) -> str:
    response = client.beta.chat.completions.parse(
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
    return response.choices[0].message.parsed
