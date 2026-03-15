#!/usr/bin/env python3
"""X Rewriter – Research trending X posts and rewrite them."""

import argparse
import sys

from rewriter import STRATEGIES, rewrite, show_rewrites
from scraper import fetch_tweet_text, research_topic


def cmd_search(args: argparse.Namespace) -> None:
    """Search for popular posts and show rewrite suggestions."""
    posts = research_topic(args.keyword, max_results=args.count)
    if not posts:
        print("投稿が見つかりませんでした。別のキーワードを試してください。")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"🎯 「{args.keyword}」の人気投稿 → リライト候補")
    print(f"{'=' * 60}")

    for i, post in enumerate(posts):
        print(f"\n--- 投稿 {i + 1} (@{post['username']}) ---")
        print(f"  URL: {post['url']}")
        print(f"  原文: {post['text'][:200]}")

        rewrites = rewrite(post["text"], strategy=args.style)
        show_rewrites(post["text"], rewrites)

    # Save results
    if args.output:
        _save_results(posts, args)


def cmd_rewrite(args: argparse.Namespace) -> None:
    """Rewrite a single tweet by URL or direct text input."""
    if args.url:
        print(f"🔗 {args.url} の本文を取得中...")
        text = fetch_tweet_text(args.url)
        if not text:
            print("ツイート本文を取得できませんでした。", file=sys.stderr)
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        print("--url または --text を指定してください。", file=sys.stderr)
        sys.exit(1)

    rewrites = rewrite(text, strategy=args.style)
    show_rewrites(text, rewrites)


def cmd_styles(args: argparse.Namespace) -> None:
    """List available rewrite styles."""
    print("\n📋 利用可能なリライトスタイル:\n")
    for name, (desc, _) in STRATEGIES.items():
        print(f"  {name:12s} – {desc}")
    print()


def _save_results(posts: list[dict], args: argparse.Namespace) -> None:
    """Save search + rewrite results to a text file."""
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# X Rewriter Results: 「{args.keyword}」\n\n")
        for i, post in enumerate(posts):
            f.write(f"## 投稿 {i + 1} (@{post['username']})\n")
            f.write(f"URL: {post['url']}\n")
            f.write(f"原文: {post['text']}\n\n")
            rewrites = rewrite(post["text"], strategy=args.style)
            for name, text in rewrites.items():
                desc = STRATEGIES[name][0]
                f.write(f"### [{name}] {desc}\n")
                f.write(f"{text}\n\n")
            f.write("---\n\n")
    print(f"\n💾 結果を {args.output} に保存しました。")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="X (Twitter) の人気投稿をリサーチしてリライト"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- search command ---
    search_p = subparsers.add_parser(
        "search", help="キーワードで人気投稿を検索してリライト"
    )
    search_p.add_argument("keyword", help="検索キーワード")
    search_p.add_argument(
        "-n", "--count", type=int, default=5, help="取得件数 (default: 5)"
    )
    search_p.add_argument(
        "-s", "--style", choices=list(STRATEGIES.keys()),
        help="リライトスタイル (省略時: 全スタイル表示)"
    )
    search_p.add_argument(
        "-o", "--output", help="結果をファイルに保存"
    )
    search_p.set_defaults(func=cmd_search)

    # --- rewrite command ---
    rw_p = subparsers.add_parser(
        "rewrite", help="指定したツイートをリライト"
    )
    rw_group = rw_p.add_mutually_exclusive_group(required=True)
    rw_group.add_argument("--url", help="ツイートのURL")
    rw_group.add_argument("--text", help="リライトしたいテキスト")
    rw_p.add_argument(
        "-s", "--style", choices=list(STRATEGIES.keys()),
        help="リライトスタイル (省略時: 全スタイル表示)"
    )
    rw_p.set_defaults(func=cmd_rewrite)

    # --- styles command ---
    styles_p = subparsers.add_parser("styles", help="リライトスタイル一覧")
    styles_p.set_defaults(func=cmd_styles)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
