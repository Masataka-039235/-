"""Schedule tweets from a JSON file."""

import json
import sys
import time
from datetime import datetime, timezone

from x_poster import get_client


def run_schedule(schedule_file: str) -> None:
    """Read a schedule JSON file and post tweets at specified times.

    Schedule file format:
    [
        {"time": "2026-03-15T10:00:00+09:00", "text": "Hello from scheduler!"},
        {"time": "2026-03-15T12:00:00+09:00", "text": "Afternoon tweet"}
    ]
    """
    try:
        with open(schedule_file) as f:
            entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading schedule file: {e}", file=sys.stderr)
        sys.exit(1)

    if not entries:
        print("Schedule file is empty.", file=sys.stderr)
        sys.exit(1)

    # Parse and sort by time
    scheduled = []
    for entry in entries:
        try:
            post_time = datetime.fromisoformat(entry["time"])
            if post_time.tzinfo is None:
                post_time = post_time.replace(tzinfo=timezone.utc)
            scheduled.append({"time": post_time, "text": entry["text"]})
        except (KeyError, ValueError) as e:
            print(f"Invalid entry: {entry} ({e})", file=sys.stderr)
            sys.exit(1)

    scheduled.sort(key=lambda x: x["time"])

    client = get_client()
    print(f"Loaded {len(scheduled)} scheduled tweets.")

    for item in scheduled:
        now = datetime.now(timezone.utc)
        wait_seconds = (item["time"] - now).total_seconds()

        if wait_seconds > 0:
            print(
                f"Next tweet at {item['time'].isoformat()} "
                f"(waiting {wait_seconds:.0f}s)..."
            )
            time.sleep(wait_seconds)

        text = item["text"]
        try:
            response = client.create_tweet(text=text)
            tweet_id = response.data["id"]
            print(f"[{datetime.now(timezone.utc).isoformat()}] Posted: {text[:50]}...")
            print(f"  -> https://x.com/i/status/{tweet_id}")
        except Exception as e:
            print(f"Failed to post: {text[:50]}... Error: {e}", file=sys.stderr)
