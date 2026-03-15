"""Rewrite tweets using various patterns – no LLM API required."""

import random
import re


# ---------------------------------------------------------------------------
# Rewrite strategies
# ---------------------------------------------------------------------------

def _reverse_viewpoint(text: str) -> str:
    """Flip the perspective (e.g. positive ↔ negative framing)."""
    swaps = [
        ("メリット", "注意点"), ("注意点", "メリット"),
        ("良い", "気をつけたい"), ("悪い", "見直したい"),
        ("成功", "成長"), ("失敗", "学び"),
        ("簡単", "奥が深い"), ("難しい", "やりがいがある"),
        ("好き", "気になる"), ("嫌い", "苦手意識がある"),
        ("最高", "かなり良い"), ("最悪", "改善の余地がある"),
    ]
    result = text
    for old, new in swaps:
        result = result.replace(old, new)
    return result


def _add_hook(text: str) -> str:
    """Add an attention-grabbing hook at the beginning."""
    hooks = [
        "知らないと損する話。\n\n",
        "これ、マジで知ってほしい。\n\n",
        "意外と知られてないけど、\n\n",
        "ぶっちゃけ言うと、\n\n",
        "周りに差をつけたいなら。\n\n",
        "今日から使える知識。\n\n",
        "結論から言うと、\n\n",
        "これだけは覚えておいて。\n\n",
    ]
    return random.choice(hooks) + text


def _listicle(text: str) -> str:
    """Convert text into a numbered list format."""
    # Split by sentence-ending punctuation
    sentences = re.split(r"[。\.\n]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if len(sentences) <= 1:
        return f"ポイントまとめ：\n\n① {text}"

    lines = []
    markers = ["①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩"]
    for i, sentence in enumerate(sentences[:10]):
        lines.append(f"{markers[i]} {sentence}")

    return "\n".join(lines)


def _question_style(text: str) -> str:
    """Reframe as a question to boost engagement."""
    openers = [
        "みんなはどう思う？\n\n",
        "これ、共感できる人いる？\n\n",
        "あなたはどっち派？\n\n",
        "正直、どう思いますか？\n\n",
    ]
    closers = [
        "\n\nリプで教えて！",
        "\n\n共感したらRT！",
        "\n\nみんなの意見聞きたい。",
        "\n\n当てはまる人いいね！",
    ]
    return random.choice(openers) + text + random.choice(closers)


def _storytelling(text: str) -> str:
    """Wrap the message in a short narrative frame."""
    intros = [
        "昔の自分に伝えたいこと。\n\n",
        "3年前の自分は知らなかった。\n\n",
        "先日こんなことがあった。\n\n",
        "最近気づいたんだけど、\n\n",
    ]
    outros = [
        "\n\nもっと早く知りたかった。",
        "\n\nこれに気づいてから変わった。",
        "\n\n同じ経験した人いるかな。",
    ]
    return random.choice(intros) + text + random.choice(outros)


def _concise(text: str) -> str:
    """Shorten the text to a punchy one-liner."""
    sentences = re.split(r"[。\.\n]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return text
    # Pick the most impactful sentence (longest as a rough proxy)
    core = max(sentences, key=len)
    return core + "。"


# ---------------------------------------------------------------------------
# Public interface
# ---------------------------------------------------------------------------

STRATEGIES = {
    "hook": ("フック追加 – 冒頭に目を引く一文を追加", _add_hook),
    "list": ("リスト化 – 箇条書きに変換", _listicle),
    "question": ("質問型 – 問いかけ形式でエンゲージメント向上", _question_style),
    "story": ("ストーリー型 – 体験談風にリフレーム", _storytelling),
    "reverse": ("視点変換 – 表現を別の角度に言い換え", _reverse_viewpoint),
    "concise": ("簡潔化 – 最もインパクトのある一文に凝縮", _concise),
}


def rewrite(text: str, strategy: str | None = None) -> dict[str, str]:
    """Rewrite a tweet using the specified strategy (or all strategies).

    Returns dict mapping strategy name → rewritten text.
    """
    if strategy and strategy in STRATEGIES:
        _, fn = STRATEGIES[strategy]
        result = fn(text)
        # Truncate to 280 chars
        if len(result) > 280:
            result = result[:277] + "..."
        return {strategy: result}

    # Apply all strategies
    results = {}
    for name, (_, fn) in STRATEGIES.items():
        result = fn(text)
        if len(result) > 280:
            result = result[:277] + "..."
        results[name] = result
    return results


def show_rewrites(original: str, rewrites: dict[str, str]) -> None:
    """Pretty-print rewrite results."""
    print("\n" + "=" * 60)
    print("📝 元の投稿:")
    print(f"  {original[:200]}")
    print("=" * 60)

    for name, text in rewrites.items():
        desc = STRATEGIES[name][0]
        char_count = len(text)
        print(f"\n🔄 [{name}] {desc}")
        print(f"   ({char_count}文字)")
        print("-" * 40)
        for line in text.split("\n"):
            print(f"  {line}")

    print("\n" + "=" * 60)
