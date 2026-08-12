from linebot.models import TextMessage
from datetime import datetime, date
from sqlalchemy.orm import Session
from models import User, Record
from claude_integration import generate_motivation_message

def handle_message(event, session: Session, line_bot_api):
    """LINEメッセージを処理"""
    user_id = event.source.user_id
    message_text = event.message.text

    # ユーザーを取得または作成
    user = session.query(User).filter_by(line_user_id=user_id).first()
    if not user:
        profile = line_bot_api.get_profile(user_id)
        user = User(
            line_user_id=user_id,
            display_name=profile.display_name
        )
        session.add(user)
        session.commit()

    # 本日の記録を取得または作成
    today = date.today()
    record = session.query(Record).filter_by(
        user_id=user.id,
        date=today
    ).first()

    if not record:
        record = Record(user_id=user.id, date=today, state='waiting_todo')
        session.add(record)
        session.commit()

    # 状態に応じた処理
    if record.state == 'waiting_todo':
        # 今日やることを待機中
        record.todo = message_text
        record.state = 'waiting_done'
        session.commit()

        # 励ましメッセージを生成
        motivation = generate_motivation_message(message_text, user.display_name)
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=f"{motivation}\n\nところで、昨日のやったことは何ですか？")
        )

    elif record.state == 'waiting_done':
        # 昨日のやったことを待機中
        record.done = message_text
        record.state = 'completed'
        session.commit()

        # 記録完了メッセージ
        summary = f"【本日の記録】\n✅ 今日やること: {record.todo}\n✅ 昨日のやったこと: {record.done}\n\n頑張ってください！"
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text=summary)
        )

    elif record.state == 'completed':
        # 既に本日分が記録されている場合
        line_bot_api.reply_message(
            event.reply_token,
            TextMessage(text="今日の記録はもう済んでますね！明日の朝に新しい記録をスタートします。")
        )
