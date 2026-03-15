# X Auto Poster

X (Twitter) への自動投稿ツール。CLI からの手動投稿と、JSON ファイルによるスケジュール投稿に対応。

## セットアップ

### 1. X API キーの取得

1. [X Developer Portal](https://developer.x.com/en/portal/dashboard) にアクセス
2. プロジェクトとアプリを作成
3. 「User authentication settings」で **Read and Write** 権限を設定
4. 以下の4つのキーを取得:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret

### 2. インストール

```bash
cd x-auto-poster
pip install -r requirements.txt
cp .env.example .env
```

### 3. 認証情報の設定

`.env` ファイルを編集して、取得したキーを入力:

```
X_API_KEY=your_api_key_here
X_API_SECRET=your_api_secret_here
X_ACCESS_TOKEN=your_access_token_here
X_ACCESS_TOKEN_SECRET=your_access_token_secret_here
```

## 使い方

### 手動投稿

```bash
python x_poster.py post "Hello from X Auto Poster!"
```

### スケジュール投稿

1. スケジュールファイル (JSON) を作成:

```json
[
    {"time": "2026-03-15T10:00:00+09:00", "text": "朝のツイート"},
    {"time": "2026-03-15T12:00:00+09:00", "text": "昼のツイート"}
]
```

2. 実行:

```bash
python x_poster.py schedule schedule_example.json
```

プログラムが起動し続け、指定時刻になると自動で投稿します。
