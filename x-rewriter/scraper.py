"""Search for popular X posts using DuckDuckGo (no API key required)."""

from __future__ import annotations

import re
import time
from dataclasses import dataclass
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ja,en;q=0.9",
}

# Pattern to match X/Twitter post URLs
X_URL_PATTERN = re.compile(
    r"https?://(?:x\.com|twitter\.com)/(\w+)/status/(\d+)"
)


@dataclass
class SearchResult:
    url: str
    username: str
    tweet_id: str
    snippet: str


def search_popular_posts(keyword: str, max_results: int = 10) -> list[SearchResult]:
    """Search DuckDuckGo for popular X posts matching a keyword."""
    query = quote_plus(f"site:x.com {keyword}")
    url = f"https://html.duckduckgo.com/html/?q={query}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Search error: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results: list[SearchResult] = []

    for result_div in soup.select(".result"):
        link_tag = result_div.select_one(".result__a")
        snippet_tag = result_div.select_one(".result__snippet")

        if not link_tag:
            continue

        href = link_tag.get("href", "")
        # DuckDuckGo sometimes wraps URLs in redirects
        if "uddg=" in href:
            from urllib.parse import parse_qs, urlparse

            parsed = urlparse(href)
            params = parse_qs(parsed.query)
            href = params.get("uddg", [href])[0]

        match = X_URL_PATTERN.search(href)
        if not match:
            continue

        username = match.group(1)
        tweet_id = match.group(2)
        snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""

        results.append(
            SearchResult(
                url=f"https://x.com/{username}/status/{tweet_id}",
                username=username,
                tweet_id=tweet_id,
                snippet=snippet,
            )
        )

        if len(results) >= max_results:
            break

    return results


def fetch_tweet_text(tweet_url: str) -> str | None:
    """Fetch tweet text using X's oEmbed endpoint (no API key needed)."""
    oembed_url = "https://publish.twitter.com/oembed"
    params = {"url": tweet_url, "omit_script": "true", "lang": "ja"}

    try:
        resp = requests.get(oembed_url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException:
        return None

    # Extract text from the HTML response
    html = data.get("html", "")
    soup = BeautifulSoup(html, "html.parser")

    # The tweet text is inside <p> tags within the blockquote
    blockquote = soup.find("blockquote")
    if not blockquote:
        return None

    paragraphs = blockquote.find_all("p")
    text_parts = [p.get_text(strip=True) for p in paragraphs]
    return "\n".join(text_parts) if text_parts else None


def research_topic(keyword: str, max_results: int = 10) -> list[dict]:
    """Search for popular posts and fetch their full text.

    Returns list of dicts with keys: url, username, tweet_id, text
    """
    print(f"\n🔍 「{keyword}」で人気投稿を検索中...\n")
    search_results = search_popular_posts(keyword, max_results=max_results)

    if not search_results:
        print("検索結果が見つかりませんでした。")
        return []

    print(f"  {len(search_results)} 件の投稿が見つかりました。本文を取得中...\n")

    posts = []
    for i, result in enumerate(search_results):
        text = fetch_tweet_text(result.url)
        if text:
            posts.append(
                {
                    "url": result.url,
                    "username": result.username,
                    "tweet_id": result.tweet_id,
                    "text": text,
                }
            )
            print(f"  [{i + 1}] @{result.username}: {text[:60]}...")
        else:
            # Fall back to search snippet
            if result.snippet:
                posts.append(
                    {
                        "url": result.url,
                        "username": result.username,
                        "tweet_id": result.tweet_id,
                        "text": result.snippet,
                    }
                )
                print(f"  [{i + 1}] @{result.username}: {result.snippet[:60]}... (snippet)")

        # Be polite to servers
        time.sleep(0.5)

    return posts
