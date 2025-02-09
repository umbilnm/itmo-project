import os
from typing import List

from dotenv import load_dotenv

from llm import agent_plan, answer_with_context, raw_answer

from .tavily_agent import TavilyAgent

load_dotenv()


class ITMOSearchAgent:
    def __init__(self):
        self.tavily_agent = TavilyAgent(api_key=os.getenv("TAVILY_API_KEY"))

    async def get_answer(self, query: str):
        """
        Ответ на вопрос о ИТМО

        """
        agent_answer = await agent_plan(query)
        self.choose_answer = agent_answer.choose_answer
        if agent_answer.confidence_level > 8:
            return await raw_answer(query)
        else:
            context = await self.get_context_from_tools(agent_answer.question)
            return await answer_with_context(query, context)

    async def get_context_from_tools(self, query: str):
        """
        Получение контекста из инструментов
        """

        context = await self.tavily_agent.fetch_tavily(query)
        return context
