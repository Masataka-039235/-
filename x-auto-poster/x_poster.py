#!/usr/bin/env python3
"""X (Twitter) auto-poster tool – post from CLI or schedule tweets."""

import argparse
import sys

import tweepy
from config import load_config


def get_client() -> tweepy.Client:
    """Authenticate and return a tweepy v2 Client."""
    cfg = load_config()
    return tweepy.Client(
        consumer_key=cfg["api_key"],
        consumer_secret=cfg["api_secret"],
        access_token=cfg["access_token"],
        access_token_secret=cfg["access_token_secret"],
    )


def post_tweet(text: str) -> None:
    """Post a single tweet."""
    if len(text) > 280:
        print(f"Error: Tweet is {len(text)} chars (max 280).", file=sys.stderr)
        sys.exit(1)

    client = get_client()
    response = client.create_tweet(text=text)
    tweet_id = response.data["id"]
    print(f"Posted! https://x.com/i/status/{tweet_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Post to X (Twitter)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- post command ---
    post_parser = subparsers.add_parser("post", help="Post a tweet immediately")
    post_parser.add_argument("text", help="Tweet text (max 280 chars)")

    # --- schedule command ---
    sched_parser = subparsers.add_parser(
        "schedule", help="Post tweets on a schedule from a file"
    )
    sched_parser.add_argument(
        "file", help="Path to schedule file (JSON)"
    )

    args = parser.parse_args()

    if args.command == "post":
        post_tweet(args.text)
    elif args.command == "schedule":
        from scheduler import run_schedule

        run_schedule(args.file)


if __name__ == "__main__":
    main()
