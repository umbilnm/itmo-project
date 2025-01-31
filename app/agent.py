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
        agent_answer = agent_plan(query)
        if agent_answer.can_answer:
            return raw_answer(query)
        else:
            context = await self.get_context_from_tools(
                agent_answer.question, agent_answer.tools
            )
            return answer_with_context(query, context)

    async def get_context_from_tools(self, query: str, tools: List[int]):
        """
        Получение контекста из инструментов
        """
        if 1 in tools:
            context = await self.tavily_agent.fetch_tavily(query)
        return context

    async def _tavily_search(self, query: str) -> list[str]:
        """
        Поиск в ТАВИЛИ
        """
        results = await self.tavily_agent.search(query)
        return results
