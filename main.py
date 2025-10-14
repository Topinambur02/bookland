from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db, engine
from models.models import Base
import crud.crud as crud
import schemas.schemas as schemas
from exceptions.exceptions import BookNotFoundException
from hooks.hooks import exception_handlers

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

for exception, handler in exception_handlers.items():
    app.add_exception_handler(exception, handler)


@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в систему управления библиотекой!"}


@app.get("/branches/{branch_name}/books/{book_title}/copies")
def get_book_copies_in_branch(branch_name: str, book_title: str, db: Session = Depends(get_db)):
    copies_count = crud.get_book_copies_in_branch(db, branch_name, book_title)
    return {"branch_name": branch_name, "book_title": book_title, "copies_count": copies_count}


@app.get("/books/{book_title}/branches/{branch_name}/faculties")
def get_book_faculties_in_branch(book_title: str, branch_name: str, db: Session = Depends(get_db)):
    return crud.get_book_faculties_in_branch(db, book_title, branch_name)


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if not db_book:
        raise BookNotFoundException(f"Книга с ID {book_id} не найдена")
    return db_book


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book)


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    return crud.delete_book(db, book_id)


@app.post("/branches/", response_model=schemas.Branch)
def create_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    return crud.create_branch(db, branch)


@app.get("/branches/", response_model=List[schemas.Branch])
def read_branches(db: Session = Depends(get_db)):
    return crud.get_branches(db)


@app.put("/branches/{branch_id}", response_model=schemas.Branch)
def update_branch(branch_id: int, branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    return crud.update_branch(db, branch_id, branch)


@app.post("/faculties/", response_model=schemas.Faculty)
def create_faculty(faculty: schemas.FacultyCreate, db: Session = Depends(get_db)):
    return crud.create_faculty(db, faculty)


@app.get("/faculties/", response_model=List[schemas.Faculty])
def read_faculties(db: Session = Depends(get_db)):
    return crud.get_faculties(db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
