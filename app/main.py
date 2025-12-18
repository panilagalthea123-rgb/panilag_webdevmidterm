from fastapi import FastAPI, Depends
from sqlmodel import Session, select
from .database import create_db, get_session
from .models import Item

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db()

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.post("/items")
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/items")
def read_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()
