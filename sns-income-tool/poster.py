"""X投稿モジュール"""

import tweepy
from config import load_x_config


def _get_client():
    cfg = load_x_config()
    return tweepy.Client(
        consumer_key=cfg["api_key"],
        consumer_secret=cfg["api_secret"],
        access_token=cfg["access_token"],
        access_token_secret=cfg["access_token_secret"],
    )


def post_tweet(text):
    """ツイートを投稿してURLを返す"""
    if len(text) > 280:
        raise ValueError(f"文字数超過: {len(text)}/280")

    client = _get_client()
    resp = client.create_tweet(text=text)
    tweet_id = resp.data["id"]
    me = client.get_me().data
    url = f"https://x.com/{me.username}/status/{tweet_id}"
    return url


def post_thread(texts):
    """スレッド（連続ツイート）を投稿する"""
    client = _get_client()
    reply_to = None
    urls = []

    for text in texts:
        if len(text) > 280:
            raise ValueError(f"文字数超過: {len(text)}/280")
        kwargs = {"text": text}
        if reply_to:
            kwargs["in_reply_to_tweet_id"] = reply_to
        resp = client.create_tweet(**kwargs)
        reply_to = resp.data["id"]
        urls.append(reply_to)

    return urls
