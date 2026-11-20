from functools import lru_cache

from langchain_tavily import TavilySearch
from langchain_tavily._utilities import TavilySearchAPIWrapper
from langchain_firecrawl import FirecrawlScrape

from app.core.config import settings


@lru_cache(maxsize=1)
def get_tavily_search_tool() -> TavilySearch:
    if settings.tavily_api_key is None:
        raise ValueError("TAVILY_API_KEY is not configured")

    api_wrapper = TavilySearchAPIWrapper(
        tavily_api_key=settings.tavily_api_key.get_secret_value()
    )

    return TavilySearch(
        api_wrapper=api_wrapper,
        max_results=5,
        topic="general",
        search_depth="basic",
        include_raw_content=True,
    )


@lru_cache(maxsize=1)
def get_firecrawl_scrape_tool() -> FirecrawlScrape:
    if settings.firecrawl_api_key is None:
        raise ValueError("FIRECRAWL_API_KEY is not configured")

    return FirecrawlScrape(
        api_key=settings.firecrawl_api_key.get_secret_value()
    )