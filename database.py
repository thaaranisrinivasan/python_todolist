from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Enum
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime
from enum import Enum as PyEnum
 
SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"
 

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

 
class Status(str, PyEnum):
    pending = "pending"
    completed = "completed"


 
class Priority(str, PyEnum):
    low = "low"
    medium = "medium"
    high = "high"
 
 # Creatign the table 
class Task(Base):
    __tablename__ = "tasks"
 
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    status = Column(Enum(Status), default=Status.pending)
    created_at = Column(DateTime, default=datetime.now)
    due_date = Column(Date, nullable=True)
    priority = Column(Enum(Priority), default=Priority.medium)
    

 
