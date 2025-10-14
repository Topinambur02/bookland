from sqlalchemy.orm import Session
from models.models import Book, Branch, Faculty
from schemas.schemas import BookCreate, BookUpdate, BranchCreate, FacultyCreate
from exceptions.exceptions import (
    BranchNotFoundException,
    DuplicateBookException,
    FacultyNotFoundException,
    BookNotFoundException,
)


def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()


def get_books(db: Session):
    return db.query(Book).all()


def create_book(db: Session, book: BookCreate):
    branch = db.query(Branch).filter(Branch.id == book.branch_id).first()

    if not branch:
        exception_message = f"Филиал с ID {book.branch_id} не найден"
        raise BranchNotFoundException(exception_message)

    existing_book = (
        db.query(Book)
        .filter(Book.title == book.title, Book.author == book.author, Book.branch_id == book.branch_id)
        .first()
    )

    if existing_book:
        raise DuplicateBookException(f"Книга '{book.title}' уже существует в этом филиале")

    db_book = Book(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        year=book.year,
        pages=book.pages,
        illustrations=book.illustrations,
        price=book.price,
        branch_id=book.branch_id,
        copies_available=book.copies_available,
        students_borrowed_count=book.students_borrowed_count,
    )

    if book.faculty_ids:
        faculties = db.query(Faculty).filter(Faculty.id.in_(book.faculty_ids)).all()
        if len(faculties) != len(book.faculty_ids):
            raise FacultyNotFoundException("Один или несколько факультетов не найдены")
        db_book.faculties = faculties

    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


def update_book(db: Session, book_id: int, book: BookUpdate):
    db_book = get_book(db, book_id)

    if not db_book:
        raise BookNotFoundException(f"Книга с ID {book_id} не найдена")

    update_data = book.model_dump(exclude_unset=True)

    if "faculty_ids" in update_data:
        faculties = db.query(Faculty).filter(Faculty.id.in_(update_data["faculty_ids"])).all()
        if len(faculties) != len(update_data["faculty_ids"]):
            raise FacultyNotFoundException("Один или несколько факультетов не найдены")
        db_book.faculties = faculties
        del update_data["faculty_ids"]

    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)

    return db_book


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)

    if not db_book:
        raise BookNotFoundException(f"Книга с ID {book_id} не найдена")

    db.delete(db_book)
    db.commit()

    return db_book


def get_branch(db: Session, branch_id: int):
    return db.query(Branch).filter(Branch.id == branch_id).first()


def get_branches(db: Session):
    return db.query(Branch).all()


def create_branch(db: Session, branch: BranchCreate):
    db_branch = Branch(**branch.model_dump())

    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)

    return db_branch


def update_branch(db: Session, branch_id: int, branch: BranchCreate):
    db_branch = get_branch(db, branch_id)
    if not db_branch:
        raise BranchNotFoundException(f"Филиал с ID {branch_id} не найден")

    for field, value in branch.model_dump().items():
        setattr(db_branch, field, value)

    db.commit()
    db.refresh(db_branch)
    return db_branch


def create_faculty(db: Session, faculty: FacultyCreate):
    db_faculty = Faculty(**faculty.model_dump())
    db.add(db_faculty)
    db.commit()
    db.refresh(db_faculty)
    return db_faculty


def get_faculties(db: Session):
    return db.query(Faculty).all()


def get_book_copies_in_branch(db: Session, branch_name: str, book_title: str):
    branch = db.query(Branch).filter(Branch.name == branch_name).first()
    if not branch:
        raise BranchNotFoundException(f"Филиал '{branch_name}' не найден")

    book = db.query(Book).filter(Book.title == book_title, Book.branch_id == branch.id).first()

    if not book:
        return 0

    return book.copies_available


def get_book_faculties_in_branch(db: Session, book_title: str, branch_name: str):
    branch = db.query(Branch).filter(Branch.name == branch_name).first()
    if not branch:
        raise BranchNotFoundException(f"Филиал '{branch_name}' не найден")

    book = db.query(Book).filter(Book.title == book_title, Book.branch_id == branch.id).first()

    if not book:
        raise BookNotFoundException(f"Книга '{book_title}' не найдена в филиале '{branch_name}'")

    faculties = [faculty.name for faculty in book.faculties]

    return {
        "book_title": book_title,
        "branch_name": branch_name,
        "faculties_count": len(faculties),
        "faculties": faculties,
    }
