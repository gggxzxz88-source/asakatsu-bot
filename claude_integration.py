from anthropic import Anthropic
from config import Config

client = Anthropic()

def generate_motivation_message(todo: str, user_name: str) -> str:
    """Claude APIを使ってモチベーション励ましメッセージを生成"""
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=100,
            messages=[
                {
                    "role": "user",
                    "content": f"{user_name}さんが今日やることは「{todo}」だと言っています。短く（1-2文）、前向きで励ましになるような返信をしてください。絵文字を入れてください。"
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error generating motivation message: {e}")
        return "頑張ってください！"

def generate_weekly_summary(records_text: str, user_name: str) -> str:
    """Claude APIを使って週次振り返りメッセージを生成"""
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[
                {
                    "role": "user",
                    "content": f"{user_name}さんの今週の朝活記録です:\n\n{records_text}\n\nこの記録を読んで、今週の振り返りと来週へのモチベーションを高める温かいメッセージを書いてください。頑張った点を具体的に褒めて、絵文字を使ってください。300文字程度でお願いします。"
                }
            ]
        )
        return message.content[0].text
    except Exception as e:
        print(f"Error generating weekly summary: {e}")
        return "今週もお疲れ様でした！来週も一緒に頑張りましょう！"
