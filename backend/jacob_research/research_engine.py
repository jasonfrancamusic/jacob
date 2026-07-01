from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ResearchResult:
    title: str
    url: str
    snippet: str = ""
    source: str = "web"

    def as_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
        }


class ResearchEngine:
    """Simple live web research engine for Jacob OS.

    It starts with keyless DuckDuckGo HTML search. This is enough for development.
    Later we can add Serper, Tavily, Brave Search or a custom crawler.
    """

    CURRENT_KEYWORDS = (
        "hoje",
        "agora",
        "atual",
        "classificado",
        "classificados",
        "resultado",
        "resultados",
        "passaram",
        "passou",
        "últimas",
        "notícias",
        "noticias",
    )

    def __init__(self) -> None:
        self.timeout = int(os.getenv("JACOB_RESEARCH_TIMEOUT", "15"))
        self.max_results = int(os.getenv("JACOB_RESEARCH_MAX_RESULTS", "5"))

    def should_research(self, message: str) -> bool:
        text = message.lower()
        return any(keyword in text for keyword in self.CURRENT_KEYWORDS)

    def normalize_query(self, message: str, conversation_context: str = "") -> str:
        text = f"{conversation_context}\n{message}".lower()
        if "copa" in text and "mundo" in text:
            return "Copa do Mundo 2026 classificados próxima fase hoje"
        if "copa" in text:
            return "Copa do Mundo 2026 classificados hoje"
        return message

    def search(self, query: str, limit: int | None = None) -> list[ResearchResult]:
        limit = limit or self.max_results
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 JacobOS/0.2 ResearchEngine",
        }

        try:
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()
        except Exception:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results: list[ResearchResult] = []

        for result in soup.select(".result")[:limit]:
            link = result.select_one(".result__a")
            snippet = result.select_one(".result__snippet")
            if not link:
                continue

            title = link.get_text(" ", strip=True)
            href = link.get("href", "")
            text = snippet.get_text(" ", strip=True) if snippet else ""
            if title and href:
                results.append(ResearchResult(title=title, url=href, snippet=text, source="duckduckgo"))

        return results

    def format_results(self, results: list[ResearchResult]) -> str:
        if not results:
            return "Nenhum resultado de pesquisa ao vivo foi retornado."

        lines = []
        for index, result in enumerate(results, start=1):
            lines.append(
                f"{index}. {result.title}\n"
                f"Fonte: {result.url}\n"
                f"Resumo: {result.snippet or 'Sem resumo disponível.'}"
            )
        return "\n\n".join(lines)
