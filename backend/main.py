from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, database, crud, schemas

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/boards/")
def create_board(data: schemas.BoardCreate, db: Session = Depends(get_db)):
    board = models.Board(**data.dict())
    db.add(board)
    db.commit()
    db.refresh(board)
    return board

@app.get("/boards/by_name/")
def get_board_by_name(name: str, db: Session = Depends(get_db)):
    return db.query(models.Board).filter(models.Board.name.ilike(name)).first()

@app.put("/boards/{board_id}")
def update_board(board_id: int, data: schemas.BoardCreate, db: Session = Depends(get_db)):
    board = db.query(models.Board).filter(models.Board.id == board_id).first()
    if board:
        board.name = data.name  # type: ignore
        board.description = data.description  # type: ignore
        db.commit()
        db.refresh(board)
        return board
    return {"error": "No encontrado"}

@app.post("/columns/")
def create_column(data: schemas.ColumnCreate, db: Session = Depends(get_db)):
    column = models.ColumnBoard(**data.dict())
    db.add(column)
    db.commit()
    db.refresh(column)
    return column

@app.get("/columns/by_name/")
def get_column_by_name(name: str, board_id: int, db: Session = Depends(get_db)):
    return db.query(models.ColumnBoard).filter(
        models.ColumnBoard.name.ilike(name),
        models.ColumnBoard.board_id == board_id
    ).first()


@app.post("/tasks/")
def create_task(data: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = models.Task(**data.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks/by_board/{board_id}")
def get_tasks_by_board(board_id: int, db: Session = Depends(get_db)):
    return db.query(models.Task).join(models.ColumnBoard).filter(models.ColumnBoard.board_id == board_id).all()
@app.post("/checklists/")
def create_checklist(data: schemas.ChecklistCreate, db: Session = Depends(get_db)):
    checklist = models.Checklist(**data.dict())
    db.add(checklist)
    db.commit()
    db.refresh(checklist)
    return checklist
@app.post("/comments/")
def create_comment(data: schemas.CommentCreate, db: Session = Depends(get_db)):
    comment = models.Comment(**data.dict())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
@app.get("/comments/by_task/{task_id}")
def get_comments_by_task(task_id: int, db: Session = Depends(get_db)):
    return db.query(models.Comment).filter(models.Comment.task_id == task_id).all()
@app.post("/collaborators/")
def create_collaborator(data: schemas.CollaboratorCreate, db: Session = Depends(get_db)):
    collaborator = models.Collaborator(**data.dict())
    db.add(collaborator)
    db.commit()
    db.refresh(collaborator)
    return collaborator
@app.get("/collaborators/by_email/")
def get_collaborator_by_email(email: str, db: Session = Depends(get_db)):
    return db.query(models.Collaborator).filter(models.Collaborator.email.ilike(email)).first()

@app.get("/export/boards/")
def export_boards(db: Session = Depends(get_db)):
    return db.query(models.Board).all()

@app.get("/export/columns/")
def export_columns(db: Session = Depends(get_db)):
    return db.query(models.ColumnBoard).all()

@app.get("/export/tasks/")
def export_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.get("/export/comments/")
def export_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()

@app.get("/export/collaborators/")
def export_collaborators(db: Session = Depends(get_db)):
    return db.query(models.Collaborator).all()


