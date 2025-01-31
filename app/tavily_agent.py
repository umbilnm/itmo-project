import os
from typing import Dict, List

import aiohttp
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


class TavilyAgent:
    def __init__(self, api_key: str = None):
        """
        Initialize Tavily agent with API key

        Args:
            api_key (str, optional): Tavily API key. Defaults to None.
        """
        self.api_key = api_key

    async def fetch_tavily(self, query):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.tavily.com/search",
                json={
                    "query": query,
                    "num_results": 3,
                    "api_key": self.api_key,
                },
            ) as response:
                result = await response.json()
        return result

    def prepare_context(self, results: List[Dict]) -> str:
        """
        Форматирование строки
        """
        string = ""
        for result in results:
            string += result["url"] + "\n" + result["content"] + "\n"
        print(string)
        return string

    async def search(self, query: str) -> str:
        """
        Поиск в ТАВИЛИ
        """
        results = await self.fetch_tavily(query)
        return self.prepare_context(results)
