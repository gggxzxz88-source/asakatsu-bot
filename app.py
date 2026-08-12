from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from models import Base
from handlers import handle_message
from scheduler import init_scheduler

app = Flask(__name__)
app.config.from_object(Config)

# データベース初期化
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# LINE Bot設定
line_bot_api = LineBotApi(Config.LINE_CHANNEL_ACCESS_TOKEN)
webhook_handler = WebhookHandler(Config.LINE_CHANNEL_SECRET)

# スケジューラ初期化
scheduler = init_scheduler(app, Session, line_bot_api)

@app.route('/', methods=['GET'])
def health():
    """ヘルスチェック"""
    return {'status': 'ok', 'message': 'Asakatsu Bot is running'}

@app.route('/webhook', methods=['POST'])
def webhook():
    """LINE Webhook"""
    signature = request.headers.get('X-Line-Signature', '')

    try:
        webhook_handler.handle(request.get_data(as_text=True), signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@webhook_handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """テキストメッセージハンドラ"""
    session = Session()
    try:
        handle_message(event, session, line_bot_api)
    finally:
        session.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.PORT, debug=(Config.FLASK_ENV == 'development'))
