"""ツイート書き換えエンジン（6つの戦略 + 収益化テンプレート）"""

import random
import textwrap

MAX_LEN = 280


def _truncate(text):
    if len(text) <= MAX_LEN:
        return text
    return text[: MAX_LEN - 1] + "…"


# ---------------------------------------------------------------------------
# 6つのリライト戦略
# ---------------------------------------------------------------------------

def _add_hook(text):
    hooks = [
        "【知らないと損】",
        "【拡散希望】",
        "【保存推奨】",
        "これマジで有益なんだけど、",
        "9割の人が知らない事実↓\n",
        "プロが教えたがらない話↓\n",
    ]
    return _truncate(random.choice(hooks) + text)


def _listicle(text):
    sentences = [s.strip() for s in text.replace("。", "。\n").split("\n") if s.strip()]
    nums = ["①", "②", "③", "④", "⑤"]
    lines = []
    for i, s in enumerate(sentences[:5]):
        lines.append(f"{nums[i]} {s}")
    return _truncate("\n".join(lines))


def _question_style(text):
    closers = ["あなたはどう思いますか？", "知ってましたか？", "これ本当だと思う？"]
    return _truncate(f"【質問】{text}\n\n{random.choice(closers)}")


def _storytelling(text):
    openers = [
        "昔の自分に伝えたい。\n",
        "これを知って人生変わった。\n",
        "正直に言います。\n",
    ]
    return _truncate(random.choice(openers) + text)


def _reverse_viewpoint(text):
    swaps = [
        ("メリット", "注意点"), ("簡単", "奥が深い"),
        ("おすすめ", "意外な落とし穴がある"), ("最高", "実は危険"),
    ]
    result = text
    for a, b in swaps:
        if a in result:
            result = result.replace(a, b, 1)
            break
    else:
        result = f"逆の視点で言うと、{result}"
    return _truncate(result)


def _concise(text):
    sentences = [s.strip() for s in text.replace("。", "。|").split("|") if s.strip()]
    best = max(sentences, key=len) if sentences else text
    return _truncate(best)


STRATEGIES = {
    "hook": _add_hook,
    "list": _listicle,
    "question": _question_style,
    "story": _storytelling,
    "reverse": _reverse_viewpoint,
    "concise": _concise,
}


def rewrite(text, style=None):
    """指定スタイルでリライト。styleがNoneなら全スタイルで生成"""
    if style:
        fn = STRATEGIES.get(style)
        if not fn:
            raise ValueError(f"不明なスタイル: {style}")
        return {style: fn(text)}
    return {name: fn(text) for name, fn in STRATEGIES.items()}


# ---------------------------------------------------------------------------
# 収益化テンプレート
# ---------------------------------------------------------------------------

MONETIZE_TEMPLATES = {
    "affiliate": [
        "詳しくはプロフのリンクから👆",
        "気になった方はプロフのリンクへ✨",
        "リンクはプロフに貼ってあります📌",
    ],
    "lead": [
        "無料で詳しい情報をまとめました→プロフのリンクから",
        "もっと知りたい方はプロフから無料レポートをどうぞ",
    ],
    "engagement": [
        "役に立ったらRT・いいねで応援お願いします🙏",
        "保存しておくと後で役立ちます📌",
        "フォローすると毎日有益情報が届きます👀",
    ],
}


def add_monetize_cta(text, cta_type="engagement"):
    """収益化のCTA（Call To Action）を追加する"""
    templates = MONETIZE_TEMPLATES.get(cta_type, MONETIZE_TEMPLATES["engagement"])
    cta = random.choice(templates)
    combined = f"{text}\n\n{cta}"
    return _truncate(combined)
