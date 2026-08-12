# 朝活記録チャットアプリ (Asakatsu Bot)

毎朝LINEで「今日やることは？」と促されて、返信すると記録が溜まるアプリです。Claudeがモチベーション励ましメッセージを生成してくれます。

## セットアップ

### 1. 環境構築
```bash
cd asakatsu_bot
python -m venv venv
source venv/bin/activate  # macOS/Linux
# または
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 2. 環境変数設定
```bash
cp .env.example .env
```

`.env` ファイルに以下を入力：
- `LINE_CHANNEL_ACCESS_TOKEN`: LINE Developer ConsoleのChannel Access Token
- `LINE_CHANNEL_SECRET`: LINE Developer ConsoleのChannel Secret
- `CLAUDE_API_KEY`: Anthropic APIキー

### 3. データベース初期化
アプリ起動時に自動的にデータベースが作成されます。

### 4. ローカルテスト（ngrok使用）
```bash
# ターミナル1: Flaskアプリ起動
python app.py

# ターミナル2: ngrokでトンネル作成
ngrok http 5000

# LINE Developer Consoleで Webhook URLを設定
# https://xxxxx.ngrok.io/webhook (ngrokが表示するURL)
```

## 機能

### 毎朝のリマインダー
- 設定時間（デフォルト08:00）に全ユーザーにLINE通知
- 「今日やることは？」と聞かれる

### 会話フロー
1. ユーザー：「〇〇をやる」
2. Bot：「いいね！」（Claude生成）+ 「昨日のやったことは？」
3. ユーザー：「△△ができた」
4. Bot：「【本日の記録】」と表示して完了

### データ蓄積
- SQLiteに記録が溜まっていく
- ユーザーごと、日付ごとに整理

## 設定

### リマインダー時間変更
`.env` で以下を変更：
```
REMINDER_HOUR=8
REMINDER_MINUTE=0
```

### データベース変更
SQLiteからPostgreSQLに変更したい場合：
```env
DATABASE_URL=postgresql://user:password@localhost/asakatsu
```

## デプロイ

### Heroku（推奨）
```bash
heroku create your-app-name
heroku config:set LINE_CHANNEL_ACCESS_TOKEN=xxx
heroku config:set LINE_CHANNEL_SECRET=xxx
heroku config:set CLAUDE_API_KEY=xxx
git push heroku main
```

### Railway.app
Railway.appダッシュボードで新しいプロジェクト作成 → GitHubリポジトリを接続 → 環境変数設定

## トラブルシューティング

### LINEで返信がない
- `LINE_CHANNEL_ACCESS_TOKEN`, `LINE_CHANNEL_SECRET` が正しいか確認
- Webhook URLが正しく設定されているか確認（ngrokの場合は30分で変わることに注意）

### スケジューラが動かない
- タイムゾーン設定を確認（APScheduler デフォルトはUTC）
- `.env` の `REMINDER_HOUR`, `REMINDER_MINUTE` を確認

### Claudeが返信を生成しない
- `CLAUDE_API_KEY` が正しいか確認
- API使用量が上限に達していないか確認

## ファイル構成

```
asakatsu_bot/
├── app.py              # メインアプリケーション
├── models.py           # SQLAlchemyモデル定義
├── config.py           # 環境変数・設定読み込み
├── handlers.py         # LINEメッセージハンドラ
├── claude_integration.py  # Claude API連携
├── scheduler.py        # 定期実行スケジューラ
├── requirements.txt
├── .env.example
└── README.md
```

## ライセンス
MIT

## 今後の拡張
- [ ] 週単位・月単位のサマリー機能
- [ ] Webダッシュボード（進捗表示）
- [ ] 連続記録数カウント
- [ ] 友人とのシェア機能
# asakatsu-bot
