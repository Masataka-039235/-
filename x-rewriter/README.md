# X Rewriter

X (Twitter) で伸びている投稿をリサーチし、リライトするツール。**APIキー不要**。

## セットアップ

```bash
cd x-rewriter
pip install -r requirements.txt
```

## 使い方

### 1. キーワード検索 → リライト

```bash
# 「副業」に関する人気投稿を検索してリライト
python x_rewriter.py search "副業"

# 件数指定・スタイル指定・ファイル保存
python x_rewriter.py search "プログラミング 初心者" -n 10 -s hook -o results.txt
```

### 2. 特定のツイートをリライト

```bash
# URL指定
python x_rewriter.py rewrite --url "https://x.com/user/status/123456789"

# テキスト直接入力
python x_rewriter.py rewrite --text "元のツイートテキストをここに入力"

# スタイル指定
python x_rewriter.py rewrite --text "テキスト" -s question
```

### 3. リライトスタイル一覧

```bash
python x_rewriter.py styles
```

## リライトスタイル

| スタイル | 説明 |
|---------|------|
| `hook` | 冒頭に目を引くフレーズを追加 |
| `list` | 箇条書き（リスト）形式に変換 |
| `question` | 問いかけ形式でエンゲージメント向上 |
| `story` | 体験談・ストーリー風にリフレーム |
| `reverse` | 視点を変えて別の角度から表現 |
| `concise` | 最もインパクトのある一文に凝縮 |

## 仕組み

1. **検索**: DuckDuckGo で `site:x.com` 検索 → 人気投稿のURLを取得
2. **本文取得**: X の oEmbed エンドポイント（無料・認証不要）でツイート本文を取得
3. **リライト**: 6種類のパターンで自動リライト（280文字以内に調整）
