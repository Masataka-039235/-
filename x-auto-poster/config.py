"""Load X API credentials from .env file."""

import os
import sys

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv is required. Run: pip install python-dotenv", file=sys.stderr)
    sys.exit(1)


def load_config() -> dict[str, str]:
    """Load API credentials from .env file and return as dict."""
    load_dotenv()

    keys = ["API_KEY", "API_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]
    cfg = {}
    missing = []

    for key in keys:
        value = os.getenv(f"X_{key}", "")
        if not value:
            missing.append(f"X_{key}")
        cfg[key.lower()] = value

    if missing:
        print(
            f"Error: Missing environment variables: {', '.join(missing)}\n"
            "Copy .env.example to .env and fill in your credentials.",
            file=sys.stderr,
        )
        sys.exit(1)

    return cfg
