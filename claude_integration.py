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
