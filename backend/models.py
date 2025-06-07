from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    columns = relationship("ColumnBoard", back_populates="board")

class Collaborator(Base):
    __tablename__ = "collaborators"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class ColumnBoard(Base):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    board_id = Column(Integer, ForeignKey("boards.id"))
    board = relationship("Board", back_populates="columns")
    tasks = relationship("Task", back_populates="column")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    status = Column(String)
    column_id = Column(Integer, ForeignKey("columns.id"))
    column = relationship("ColumnBoard", back_populates="tasks")
    checklists = relationship("Checklist", back_populates="task")
    comments = relationship("Comment", back_populates="task")

class Checklist(Base):
    __tablename__ = "checklists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    done = Column(Boolean, default=False)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="checklists")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    date = Column(DateTime, default=datetime.utcnow)
    collaborator_id = Column(Integer, ForeignKey("collaborators.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="comments")
