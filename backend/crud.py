from sqlalchemy.orm import Session
import models, schemas

# ====== BOARDS ======
def create_board(db: Session, name: str, description: str = ""):
    board = models.Board(name=name, description=description)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board

# ====== COLUMNS ======
def create_column(db: Session, name: str, description: str, board_id: int):
    column = models.ColumnBoard(name=name, description=description, board_id=board_id)
    db.add(column)
    db.commit()
    db.refresh(column)
    return column

# ====== TASKS ======
def create_task(db: Session, task_data: schemas.TaskCreate):
    task = models.Task(
        title=task_data.title,
        description=task_data.description,
        start_date=task_data.start_date,
        end_date=task_data.end_date,
        status=task_data.status,
        column_id=task_data.column_id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

# ====== CHECKLIST ======
def create_checklist(db: Session, item: schemas.ChecklistCreate):
    checklist = models.Checklist(
        name=item.name,
        done=item.done,
        task_id=item.task_id
    )
    db.add(checklist)
    db.commit()
    db.refresh(checklist)
    return checklist

# ====== COMMENTS ======
def create_comment(db: Session, comment: schemas.CommentCreate):
    comentario = models.Comment(
        content=comment.content,
        collaborator_id=comment.collaborator_id,
        task_id=comment.task_id
    )
    db.add(comentario)
    db.commit()
    db.refresh(comentario)
    return comentario

# ====== COLLABORATORS ======
def create_collaborator(db: Session, col: schemas.CollaboratorCreate):
    collaborator = models.Collaborator(
        name=col.name,
        email=col.email
    )
    db.add(collaborator)
    db.commit()
    db.refresh(collaborator)
    return collaborator
