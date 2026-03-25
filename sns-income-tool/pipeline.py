"""収益化パイプライン: リサーチ → リライト → 収益化CTA追加 → 投稿キュー生成"""

import json
import os
import random
from datetime import datetime, timedelta

from scraper import research_topic
from rewriter import rewrite, add_monetize_cta, STRATEGIES
from config import GOLDEN_HOURS, NICHES


def generate_content(keyword, count=5, style=None, cta_type="engagement"):
    """キーワードからバズ投稿をリサーチし、リライト済みコンテンツを生成する"""
    posts = research_topic(keyword, count=count * 2)
    contents = []

    for post in posts[:count]:
        original = post["text"]
        chosen_style = style or random.choice(list(STRATEGIES.keys()))
        rewritten = rewrite(original, chosen_style)
        text = list(rewritten.values())[0]
        final = add_monetize_cta(text, cta_type)

        contents.append({
            "original_url": post["url"],
            "original_text": original,
            "style": chosen_style,
            "rewritten": text,
            "final": final,
        })

    return contents


def build_weekly_schedule(niche, posts_per_day=4, days=7, cta_type="engagement"):
    """1週間分の投稿スケジュールを自動生成する"""
    keywords = NICHES.get(niche)
    if not keywords:
        raise ValueError(f"不明なジャンル: {niche} (選択肢: {list(NICHES.keys())})")

    schedule = []
    base_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    base_date += timedelta(days=1)  # 明日から

    for day_offset in range(days):
        date = base_date + timedelta(days=day_offset)
        keyword = random.choice(keywords)
        contents = generate_content(keyword, count=posts_per_day, cta_type=cta_type)

        hours = GOLDEN_HOURS[:posts_per_day]
        for i, content in enumerate(contents):
            post_time = date.replace(hour=hours[i % len(hours)], minute=random.randint(0, 15))
            schedule.append({
                "time": post_time.isoformat(),
                "text": content["final"],
                "keyword": keyword,
                "style": content["style"],
                "original_url": content["original_url"],
            })

    return schedule


def save_schedule(schedule, filepath="data/schedule.json"):
    """スケジュールをJSONファイルに保存する"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    return filepath


def load_schedule(filepath="data/schedule.json"):
    """保存済みスケジュールを読み込む"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)
