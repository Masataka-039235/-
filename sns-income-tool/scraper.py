"""バズツイートのリサーチ・収集モジュール"""

import re
import requests
from bs4 import BeautifulSoup

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

HEADERS = {"User-Agent": USER_AGENT}

X_URL_PATTERN = re.compile(
    r"https?://(?:x|twitter)\.com/(\w+)/status/(\d+)"
)


def search_popular_posts(keyword, count=10):
    """DuckDuckGoでバズったX投稿を検索する"""
    query = f"site:x.com {keyword}"
    url = "https://html.duckduckgo.com/html/"
    resp = requests.post(url, data={"q": query}, headers=HEADERS, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    for a_tag in soup.select("a.result__a"):
        href = a_tag.get("href", "")
        match = X_URL_PATTERN.search(href)
        if match:
            results.append({
                "url": f"https://x.com/{match.group(1)}/status/{match.group(2)}",
                "username": match.group(1),
                "tweet_id": match.group(2),
            })
        if len(results) >= count:
            break

    return results


def fetch_tweet_text(tweet_url):
    """oEmbedエンドポイントでツイート本文を取得する"""
    oembed_url = "https://publish.twitter.com/oembed"
    params = {"url": tweet_url, "omit_script": "true"}
    try:
        resp = requests.get(oembed_url, params=params, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        html = data.get("html", "")
        soup = BeautifulSoup(html, "html.parser")
        blockquote = soup.find("blockquote")
        if blockquote:
            for a in blockquote.find_all("a"):
                a.decompose()
            text = blockquote.get_text(strip=True)
            # Remove trailing "— Name (@handle) Date" part
            text = re.sub(r"\s*—\s*.+$", "", text)
            return text
    except Exception:
        pass
    return None


def research_topic(keyword, count=10):
    """キーワードでバズ投稿をリサーチし本文も取得する"""
    posts = search_popular_posts(keyword, count)
    enriched = []
    for post in posts:
        text = fetch_tweet_text(post["url"])
        if text and len(text) > 20:
            post["text"] = text
            enriched.append(post)
    return enriched
