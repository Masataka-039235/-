#!/usr/bin/env python3
"""
SNS自動収益化ツール - メインCLI

使い方:
  python main.py research <キーワード>         バズ投稿をリサーチ
  python main.py generate <ジャンル>            1週間分の投稿を自動生成
  python main.py preview                        生成済みスケジュールをプレビュー
  python main.py run                            スケジュール通りに自動投稿
  python main.py post <テキスト>                即座に1件投稿
  python main.py stats                          パフォーマンスレポート表示
  python main.py niches                         対応ジャンル一覧
  python main.py styles                         リライトスタイル一覧
"""

import argparse
import json
import sys

from config import NICHES
from rewriter import STRATEGIES


def cmd_research(args):
    from scraper import research_topic
    from rewriter import rewrite

    print(f"🔍 「{args.keyword}」でバズ投稿をリサーチ中...\n")
    posts = research_topic(args.keyword, count=args.count)

    if not posts:
        print("投稿が見つかりませんでした。キーワードを変えて試してください。")
        return

    for i, post in enumerate(posts, 1):
        print(f"━━━ {i}. @{post['username']} ━━━")
        print(f"URL: {post['url']}")
        print(f"原文: {post['text'][:100]}...")
        print()
        rewrites = rewrite(post["text"])
        for style, text in rewrites.items():
            print(f"  [{style}] {text[:80]}...")
        print()


def cmd_generate(args):
    from pipeline import build_weekly_schedule, save_schedule

    niche = args.niche
    print(f"📝 ジャンル「{niche}」で{args.days}日分の投稿を生成中...\n")

    schedule = build_weekly_schedule(
        niche,
        posts_per_day=args.posts_per_day,
        days=args.days,
        cta_type=args.cta,
    )

    filepath = save_schedule(schedule)
    print(f"✅ {len(schedule)}件の投稿スケジュールを生成しました")
    print(f"   保存先: {filepath}")
    print()
    print("プレビュー (最初の3件):")
    for entry in schedule[:3]:
        print(f"  {entry['time'][:16]} | {entry['text'][:60]}...")
    print()
    print("次のステップ:")
    print("  python main.py preview    全件プレビュー")
    print("  python main.py run        自動投稿を開始")


def cmd_preview(args):
    from pipeline import load_schedule

    try:
        schedule = load_schedule()
    except FileNotFoundError:
        print("スケジュールが見つかりません。先に generate を実行してください。")
        return

    print(f"📋 スケジュール ({len(schedule)}件)\n")
    for i, entry in enumerate(schedule, 1):
        print(f"{i:3d}. {entry['time'][:16]} [{entry.get('style', '?')}]")
        print(f"     {entry['text'][:70]}...")
        print()


def cmd_run(args):
    from scheduler import run_scheduler

    print("🚀 自動投稿を開始します...\n")
    print("⚠️  停止するには Ctrl+C を押してください\n")
    try:
        run_scheduler()
    except KeyboardInterrupt:
        print("\n⏹️  停止しました")


def cmd_post(args):
    from poster import post_tweet
    from analytics import log_post

    text = args.text
    print(f"📤 投稿中... ({len(text)}/280文字)\n")
    url = post_tweet(text)
    log_post(text, style="manual", keyword="manual", url=url)
    print(f"✅ 投稿完了: {url}")


def cmd_stats(args):
    from analytics import print_report

    print_report()


def cmd_niches(args):
    print("📂 対応ジャンル一覧:\n")
    for niche, keywords in NICHES.items():
        print(f"  {niche}: {', '.join(keywords)}")


def cmd_styles(args):
    print("🎨 リライトスタイル一覧:\n")
    descriptions = {
        "hook": "注目を引くフック文を追加",
        "list": "箇条書き（リスト形式）に変換",
        "question": "問いかけ形式に変換",
        "story": "体験談・ストーリー形式に変換",
        "reverse": "逆の視点からのリライト",
        "concise": "最もインパクトのある一文を抽出",
    }
    for name in STRATEGIES:
        desc = descriptions.get(name, "")
        print(f"  {name:10s} - {desc}")


def main():
    parser = argparse.ArgumentParser(
        description="SNS自動収益化ツール - バズ投稿リサーチ → リライト → 自動投稿",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command")

    # research
    p_research = sub.add_parser("research", help="バズ投稿をリサーチ")
    p_research.add_argument("keyword", help="検索キーワード")
    p_research.add_argument("-n", "--count", type=int, default=5, help="取得件数")
    p_research.set_defaults(func=cmd_research)

    # generate
    p_gen = sub.add_parser("generate", help="投稿スケジュールを自動生成")
    p_gen.add_argument("niche", help="ジャンル名")
    p_gen.add_argument("-d", "--days", type=int, default=7, help="日数 (デフォルト7)")
    p_gen.add_argument("-p", "--posts-per-day", type=int, default=4, help="1日の投稿数")
    p_gen.add_argument("--cta", default="engagement", choices=["affiliate", "lead", "engagement"])
    p_gen.set_defaults(func=cmd_generate)

    # preview
    p_preview = sub.add_parser("preview", help="スケジュールをプレビュー")
    p_preview.set_defaults(func=cmd_preview)

    # run
    p_run = sub.add_parser("run", help="自動投稿を実行")
    p_run.set_defaults(func=cmd_run)

    # post
    p_post = sub.add_parser("post", help="即座に1件投稿")
    p_post.add_argument("text", help="投稿テキスト")
    p_post.set_defaults(func=cmd_post)

    # stats
    p_stats = sub.add_parser("stats", help="パフォーマンスレポート")
    p_stats.set_defaults(func=cmd_stats)

    # niches
    p_niches = sub.add_parser("niches", help="ジャンル一覧")
    p_niches.set_defaults(func=cmd_niches)

    # styles
    p_styles = sub.add_parser("styles", help="リライトスタイル一覧")
    p_styles.set_defaults(func=cmd_styles)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
