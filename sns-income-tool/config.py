"""設定管理モジュール"""

import os
from dotenv import load_dotenv

load_dotenv()


def load_x_config():
    """X API認証情報を読み込む"""
    keys = {
        "api_key": os.getenv("X_API_KEY"),
        "api_secret": os.getenv("X_API_SECRET"),
        "access_token": os.getenv("X_ACCESS_TOKEN"),
        "access_token_secret": os.getenv("X_ACCESS_TOKEN_SECRET"),
    }
    missing = [k for k, v in keys.items() if not v]
    if missing:
        raise ValueError(f"未設定の環境変数: {', '.join(missing)}")
    return keys


def load_monetize_config():
    """収益化設定を読み込む"""
    return {
        "affiliate_tag": os.getenv("AFFILIATE_TAG", ""),
        "lp_url": os.getenv("LP_URL", ""),
    }


# 投稿スケジュール（エンゲージメントが高い時間帯）
GOLDEN_HOURS = [7, 12, 18, 21]

# ジャンル別キーワード
NICHES = {
    "副業": ["副業", "在宅ワーク", "稼ぐ方法", "フリーランス"],
    "投資": ["投資", "NISA", "資産運用", "株"],
    "AI": ["AI", "ChatGPT", "生成AI", "自動化"],
    "健康": ["ダイエット", "筋トレ", "健康習慣", "睡眠"],
    "節約": ["節約", "貯金", "家計", "ポイ活"],
}
