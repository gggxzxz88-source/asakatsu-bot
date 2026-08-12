from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    line_user_id = Column(String(255), unique=True, nullable=False)
    display_name = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    records = relationship('Record', back_populates='user')

    def __repr__(self):
        return f'<User {self.display_name}>'

class Record(Base):
    __tablename__ = 'records'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    date = Column(Date, nullable=False)
    todo = Column(Text)  # 今日やること
    done = Column(Text)  # 昨日のやったこと
    state = Column(String(50), default='waiting_todo')  # waiting_todo, waiting_done, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', back_populates='records')

    def __repr__(self):
        return f'<Record {self.date} - {self.user_id}>'
