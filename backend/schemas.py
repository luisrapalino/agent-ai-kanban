from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ====== BOARDS ======
class BoardCreate(BaseModel):
    name: str
    description: Optional[str] = None

# ====== COLUMNS ======
class ColumnCreate(BaseModel):
    name: str
    description: Optional[str] = None
    board_id: int

# ====== TASKS ======
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: str
    column_id: int

# ====== CHECKLIST ======
class ChecklistCreate(BaseModel):
    name: str
    done: Optional[bool] = False
    task_id: int

# ====== COMMENTS ======
class CommentCreate(BaseModel):
    content: str
    collaborator_id: int
    task_id: int

# ====== COLLABORATORS ======
class CollaboratorCreate(BaseModel):
    name: str
    email: str
