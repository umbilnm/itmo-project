import time
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

from llm.generation import summarize, validate_pages


class DDGAgent:
    def __init__(self, max_results: int = 3):
        """
        Инициализация DDG агента

        Args:
            max_results (int): Максимальное количество результатов поиска
        """
        self.max_results = max_results

    def search(self, query: str) -> List[str]:
        """
        Поиск информации через DuckDuckGo

        Args:
            query (str): Поисковый запрос

        Returns:
            List[Dict[str, str]]: Список результатов поиска
        """
        with DDGS() as ddgs:
            ddgs_gen = ddgs.text(f"{query}", max_results=5)
        snippets = []
        titles = []
        hrefs = []
        for result in ddgs_gen:
            snippets.append(result["body"])
            titles.append(result["title"])
            hrefs.append(result["href"])
        string = self._generate_validate_string(snippets, titles, hrefs)
        chosen_pages = validate_pages(string).nums
        hrefs = [hrefs[i - 1] for i in chosen_pages]
        texts = self.parse_pages(hrefs)
        string_with_content = self._generate_string_with_info(texts, hrefs)
        summarized = summarize(string_with_content, query)
        print(summarized)

    def _generate_string_with_info(self, texts: List[str], hrefs: List[str]) -> str:
        """
        Генерация строки с содержимым страниц
        """
        print(texts)
        return "\n".join(
            f"{i+1}. По ссылке {href}\nТекст: {text}"
            for i, (text, href) in enumerate(zip(texts, hrefs))
        )

    def _generate_validate_string(
        self, snippets: List[str], titles: List[str], hrefs: List[str]
    ) -> str:
        """
        Генерация строки из результатов поиска с нумерацией
        """
        return "\n".join(
            f"{i+1}. Title: {title}\nSnippet: {snippet}\nURL: {href}"
            for i, (title, snippet, href) in enumerate(zip(titles, snippets, hrefs))
        )

    def _parse_page(self, page_link: str) -> Optional[str]:
        """
        Парсинг страницы и retry если не получилось
        """
        for _ in range(3):
            try:
                response = requests.get(page_link)
                if response.status_code == 200:
                    return BeautifulSoup(response.text, "html.parser").text
            except requests.exceptions.RequestException:
                time.sleep(0.5)
                pass
        return None

    def parse_pages(self, pages: List[str]) -> str:
        """
        Парсинг страниц
        """
        return [self._parse_page(page) for page in pages]
