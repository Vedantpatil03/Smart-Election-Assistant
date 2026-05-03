"""
Database setup and initialization
"""
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from app.config import settings

# Database URL
DATABASE_URL = settings.DATABASE_URL.replace("sqlite:///", "")

# Create engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=settings.DEBUG
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model
Base = declarative_base()


class FAQ(Base):
    """FAQ database model"""
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, unique=True, index=True)
    answer = Column(Text)
    category = Column(String)
    language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatHistory(Base):
    """Chat history database model"""
    __tablename__ = "chat_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(String)
    bot_response = Column(Text)
    language = Column(String, default="en")
    intent = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    """Initialize database with tables and seed data"""
    Base.metadata.create_all(bind=engine)
    seed_faq_data()


def seed_faq_data():
    """Seed FAQ data into database"""
    db = SessionLocal()
    
    # Check if data already exists
    if db.query(FAQ).count() > 0:
        db.close()
        return
    
    faqs = [
        FAQ(
            question="What is EVM?",
            answer="EVM stands for Electronic Voting Machine. It is a machine used to record votes electronically. It ensures accurate counting and prevents invalid votes.",
            category="voting",
            language="en"
        ),
        FAQ(
            question="What is NOTA?",
            answer="NOTA stands for None Of The Above. It is an option for voters who do not wish to vote for any candidate. Voting through NOTA is completely anonymous.",
            category="voting",
            language="en"
        ),
        FAQ(
            question="Who can vote?",
            answer="A person can vote if they are: 1) Indian citizen, 2) At least 18 years old, 3) Not disqualified under law, 4) Registered as a voter in their constituency.",
            category="eligibility",
            language="en"
        ),
        FAQ(
            question="How to register as a voter?",
            answer="To register as a voter: 1) Visit your nearest election office, 2) Fill Form 6 (for new registration), 3) Provide proof of age and address, 4) Submit documents. You can also register online at your state election website.",
            category="registration",
            language="en"
        ),
        FAQ(
            question="Where is my polling booth?",
            answer="You can find your polling booth details by: 1) Visiting the election website of your state, 2) Entering your voter ID, 3) Or by contacting your local election office. You will receive a Polling Booth Slip by post.",
            category="voting",
            language="en"
        ),
        FAQ(
            question="What documents do I need to vote?",
            answer="Bring any one of these: 1) Voter ID (EPIC), 2) Aadhaar Card, 3) Driving License, 4) Passport, 5) Ration Card, 6) Polling Booth Slip (if received).",
            category="voting",
            language="en"
        ),
        FAQ(
            question="Can I vote if I am not in my constituency?",
            answer="You can vote in your registered constituency only. However, in some cases, you can apply for postal voting or vote in person with prior permission. Contact your election office for details.",
            category="voting",
            language="en"
        ),
        FAQ(
            question="What is a Voter ID?",
            answer="Voter ID (EPIC - Electoral Photo Identity Card) is an identity card issued by the election commission. It is used to verify voters and maintain electoral roll. You can apply for it at your election office.",
            category="registration",
            language="en"
        ),
    ]
    
    db.add_all(faqs)
    db.commit()
    db.close()


def get_db():
    """Database dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
