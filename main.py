from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos/")
def create_todo(todo: models.ToDo, db: Session = Depends(get_db)):
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

@app.get("/todos/")
def read_todos(db: Session = Depends(get_db)):
    return db.query(models.ToDo).all()
