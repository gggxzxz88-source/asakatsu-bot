from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import date, timedelta
from sqlalchemy.orm import sessionmaker
from models import User, Record, Base
from config import Config
from linebot import LineBotApi
from claude_integration import generate_weekly_summary

def send_daily_reminder(session_maker, line_bot_api: LineBotApi):
    """毎朝全ユーザーにリマインダーを送信"""
    Session = session_maker
    session = Session()

    try:
        users = session.query(User).all()
        for user in users:
            # 本日の記録が既にある場合はスキップ
            existing_record = session.query(Record).filter_by(
                user_id=user.id,
                date=date.today()
            ).first()

            if existing_record:
                continue

            # 新しい記録を作成
            new_record = Record(
                user_id=user.id,
                date=date.today(),
                state='waiting_todo'
            )
            session.add(new_record)

            # LINE通知を送信
            try:
                line_bot_api.push_message(
                    user.line_user_id,
                    {
                        'type': 'text',
                        'text': '🌅 おはよう！今日やることは何ですか？'
                    }
                )
            except Exception as e:
                print(f"Error sending reminder to {user.display_name}: {e}")

        session.commit()
    except Exception as e:
        print(f"Error in send_daily_reminder: {e}")
    finally:
        session.close()

def send_weekly_summary(session_maker, line_bot_api: LineBotApi):
    """毎週、1週間分の記録をまとめてClaudeに振り返りを作らせて送信"""
    Session = session_maker
    session = Session()

    try:
        users = session.query(User).all()
        week_ago = date.today() - timedelta(days=7)

        for user in users:
            records = session.query(Record).filter(
                Record.user_id == user.id,
                Record.date >= week_ago
            ).order_by(Record.date).all()

            if not records:
                continue

            records_text = "\n".join([
                f"{r.date}: 今日やること「{r.todo or '未記録'}」 / やったこと「{r.done or '未記録'}」"
                for r in records
            ])

            summary = generate_weekly_summary(records_text, user.display_name)

            try:
                line_bot_api.push_message(
                    user.line_user_id,
                    {
                        'type': 'text',
                        'text': f"📊 今週の振り返り\n\n{summary}"
                    }
                )
            except Exception as e:
                print(f"Error sending weekly summary to {user.display_name}: {e}")

    except Exception as e:
        print(f"Error in send_weekly_summary: {e}")
    finally:
        session.close()

def init_scheduler(app, session_maker, line_bot_api: LineBotApi):
    """スケジューラを初期化"""
    scheduler = BackgroundScheduler()

    trigger = CronTrigger(
        hour=Config.REMINDER_HOUR,
        minute=Config.REMINDER_MINUTE,
        timezone='Asia/Tokyo'
    )

    scheduler.add_job(
        send_daily_reminder,
        trigger=trigger,
        args=[session_maker, line_bot_api],
        id='daily_reminder'
    )

    weekly_trigger = CronTrigger(
        day_of_week='sun',
        hour=20,
        minute=0,
        timezone='Asia/Tokyo'
    )

    scheduler.add_job(
        send_weekly_summary,
        trigger=weekly_trigger,
        args=[session_maker, line_bot_api],
        id='weekly_summary'
    )

    scheduler.start()

    # アプリケーション終了時にスケジューラを停止
    import atexit
    atexit.register(lambda: scheduler.shutdown())

    return scheduler
