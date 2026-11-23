import json
from functools import lru_cache
from langchain.tools import tool
from langchain_tavily import TavilySearch
from langchain_tavily._utilities import TavilySearchAPIWrapper
from langchain_firecrawl import FirecrawlScrape
from urllib.parse import urlsplit, urlunsplit
from app.core.config import settings

TAVILY_SCORE_THRESHOLD = 0.60
MAX_RESULTS = 3
MAX_CONTENT_LENGTH = 1500


def normalize_url(url: str) -> str:
    """Normalize URLs to identify duplicate pages."""

    parsed = urlsplit(url.strip())

    hostname = (parsed.hostname or "").lower()
    hostname = hostname.removeprefix("www.")

    port = parsed.port
    netloc = f"{hostname}:{port}" if port else hostname

    path = parsed.path.rstrip("/")

    return urlunsplit((
        parsed.scheme.lower(),
        netloc,
        path,
        parsed.query,
        "",
    ))


@lru_cache(maxsize=1)
def get_tavily_search_tool() -> TavilySearch:
    if settings.tavily_api_key is None:
        raise ValueError("TAVILY_API_KEY is not configured")

    api_wrapper = TavilySearchAPIWrapper(
        tavily_api_key=settings.tavily_api_key.get_secret_value()
    )

    return TavilySearch(
        api_wrapper=api_wrapper,
        max_results=3,
        topic="general",
        search_depth="basic",
        include_raw_content=False,
        include_answer=False,
        include_images=False,
    )


@tool
def tavily_relevant_search(query: str) -> str:
    """
    Search the web for relevant research information.

    Required argument:
    - query: A non-empty search query describing the information to find.

    Always provide the query argument when calling this tool.
    Example: {"query": "luxury hotel industry trends in Bangladesh"}
    """

    response = get_tavily_search_tool().invoke({
        "query": query,
    })

    results = response.get("results", [])

    relevant_results = [
        item
        for item in results
        if item.get("score", 0) >= TAVILY_SCORE_THRESHOLD
    ]

    unique_results = []
    seen_urls = set()

    for item in relevant_results:
        normalized_url = normalize_url(item.get("url", ""))

        if not normalized_url or normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)
        unique_results.append(item)

    if not unique_results:
        return "No relevant research results found for this query."
        
    return json.dumps(
            [
                {
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "score": item.get("score", 0),
                    "content": item.get("content", "")[:MAX_CONTENT_LENGTH],
                }
                for item in unique_results[:MAX_RESULTS]
            ],
            ensure_ascii=False,
        )
        


@lru_cache(maxsize=1)
def get_firecrawl_scrape_tool() -> FirecrawlScrape:
    if settings.firecrawl_api_key is None:
        raise ValueError("FIRECRAWL_API_KEY is not configured")

    return FirecrawlScrape(
        api_key=settings.firecrawl_api_key.get_secret_value(),
        only_main_content=True,
        formats=["markdown"],
    )


@tool
def firecrawl_article_extract(url: str) -> dict:
    """Scrape a webpage and return its metadata and article content."""

    result = get_firecrawl_scrape_tool().invoke({
        "url": url,
    })

    metadata = result.get("metadata", {})
    markdown = result.get("markdown", "")

    # Locate the article title in the extracted Markdown.
    title = metadata.get("title", "")
    title_index = markdown.find(title)

    if title_index != -1:
        markdown = markdown[title_index:]

    return {
        "title": title,
        "description": metadata.get("description", ""),
        "url": metadata.get("url", url),
        "content": markdown[:4000],
    }