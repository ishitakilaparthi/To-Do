from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
import models
import schemas

Base.metadata.create_all(engine)

app = FastAPI()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/docs")
def root():
    return "todooo"

@app.post("/todo", response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDoCreate, session: Session = Depends(get_session)):

    tododb = models.ToDo(task = todo.task)

    session.add(tododb)
    session.commit()
    session.refresh(tododb)

    return tododb


@app.get("/todo/{id}", response_model=schemas.ToDo)
def read_todo(id: int):

    session = SessionLocal()

    todo = session.query(models.ToDo).get(id)

    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo


@app.put("/todo/{id}")
def update_todo(id: int, task: str):

    session = SessionLocal()

    todo = session.query(models.ToDo).get(id)

    if todo:
        todo.task = task
        session.commit()

    session.close()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return todo

@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int):

    session = SessionLocal()

    todo = session.query(models.ToDo).get(id)

    if todo:
        session.delete(todo)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"todo item with id {id} not found")

    return None

@app.get("/todo", response_model = List[schemas.ToDo])
def read_todo_list():
    session = SessionLocal()

    todo_list = session.query(models.ToDo).all()

    session.close()

    return todo_list