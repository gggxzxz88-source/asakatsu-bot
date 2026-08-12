import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
    CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///asakatsu.db')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    PORT = int(os.getenv('PORT', 5000))
    REMINDER_HOUR = int(os.getenv('REMINDER_HOUR', 8))
    REMINDER_MINUTE = int(os.getenv('REMINDER_MINUTE', 0))

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
