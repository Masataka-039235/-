"""投稿パフォーマンス分析モジュール"""

import json
import os
from datetime import datetime

ANALYTICS_FILE = "data/analytics.json"


def _load_data():
    if os.path.exists(ANALYTICS_FILE):
        with open(ANALYTICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"posts": [], "summary": {}}


def _save_data(data):
    os.makedirs(os.path.dirname(ANALYTICS_FILE), exist_ok=True)
    with open(ANALYTICS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log_post(text, style, keyword, url=None):
    """投稿を記録する"""
    data = _load_data()
    data["posts"].append({
        "timestamp": datetime.now().isoformat(),
        "text": text,
        "style": style,
        "keyword": keyword,
        "url": url,
        "char_count": len(text),
    })
    _save_data(data)


def get_stats():
    """投稿統計を取得する"""
    data = _load_data()
    posts = data["posts"]

    if not posts:
        return {"total_posts": 0, "message": "まだ投稿データがありません"}

    style_counts = {}
    keyword_counts = {}
    for p in posts:
        style = p.get("style", "unknown")
        keyword = p.get("keyword", "unknown")
        style_counts[style] = style_counts.get(style, 0) + 1
        keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

    return {
        "total_posts": len(posts),
        "styles_used": style_counts,
        "keywords_used": keyword_counts,
        "first_post": posts[0]["timestamp"],
        "last_post": posts[-1]["timestamp"],
    }


def print_report():
    """レポートを表示する"""
    stats = get_stats()
    print("=" * 50)
    print("📊 SNS収益化ツール - パフォーマンスレポート")
    print("=" * 50)

    if stats["total_posts"] == 0:
        print("まだ投稿データがありません。")
        return

    print(f"総投稿数: {stats['total_posts']}")
    print(f"期間: {stats['first_post'][:10]} 〜 {stats['last_post'][:10]}")
    print()
    print("■ スタイル別投稿数:")
    for style, count in sorted(stats["styles_used"].items(), key=lambda x: -x[1]):
        print(f"  {style}: {count}回")
    print()
    print("■ キーワード別投稿数:")
    for kw, count in sorted(stats["keywords_used"].items(), key=lambda x: -x[1]):
        print(f"  {kw}: {count}回")

    # 月10万円の目安計算
    total = stats["total_posts"]
    print()
    print("=" * 50)
    print("💰 収益化の目安（フォロワー数に依存）")
    print("-" * 50)
    print(f"  投稿数: {total}件")
    print(f"  想定インプレッション: {total * 500:,}〜{total * 5000:,}")
    print(f"  アフィリエイト想定クリック: {total * 5}〜{total * 50}")
    print("  ※ フォロワー1万人で月4投稿/日 → 月10万円到達圏")
    print("=" * 50)
