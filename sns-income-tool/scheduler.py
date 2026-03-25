"""自動投稿スケジューラー"""

import time
from datetime import datetime

from poster import post_tweet
from pipeline import load_schedule


def run_scheduler(schedule_path="data/schedule.json"):
    """スケジュールに従って自動投稿を実行する"""
    schedule = load_schedule(schedule_path)

    # 時刻順にソート
    schedule.sort(key=lambda x: x["time"])

    print(f"📅 {len(schedule)}件の投稿がスケジュールされています")
    print("-" * 50)

    posted = 0
    skipped = 0

    for entry in schedule:
        target_time = datetime.fromisoformat(entry["time"])
        now = datetime.now()

        # 過去の投稿はスキップ
        if target_time < now:
            skipped += 1
            continue

        # 投稿時刻まで待機
        wait_seconds = (target_time - now).total_seconds()
        if wait_seconds > 0:
            print(f"⏳ 次の投稿まで {int(wait_seconds // 60)}分 待機中...")
            print(f"   予定: {target_time.strftime('%Y-%m-%d %H:%M')}")
            print(f"   内容: {entry['text'][:50]}...")
            time.sleep(wait_seconds)

        # 投稿実行
        try:
            url = post_tweet(entry["text"])
            posted += 1
            print(f"✅ 投稿完了 ({posted}件目): {url}")
        except Exception as e:
            print(f"❌ 投稿失敗: {e}")

        # API制限対策: 投稿間に60秒の間隔
        time.sleep(60)

    print("-" * 50)
    print(f"完了: 投稿{posted}件 / スキップ{skipped}件")
