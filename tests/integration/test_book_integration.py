import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Branch, Faculty
from schemas.schemas import BookCreate, BranchCreate, FacultyCreate
from exceptions.exceptions import DuplicateBookException
from crud.crud import (
    get_book, get_books, create_book, delete_book,
    get_branch, get_branches, create_branch,
    create_faculty, get_faculties, get_book_copies_in_branch,
    get_book_faculties_in_branch
)


@pytest.fixture
def db_session():
    DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/bookland"
    
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    transaction = connection.begin()
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
    engine.dispose()


class TestBookIntegration:
    def test_create_and_get_book(self, db_session):
        branch = Branch(name="Main Branch", address="123 Main St")
        db_session.add(branch)
        db_session.commit()
        
        book_data = BookCreate(
            title="Integration Test Book",
            author="Test Author",
            publisher="Test Publisher",
            year=2023,
            pages=100,
            illustrations=True,
            price=29.99,
            branch_id=branch.id,
            copies_available=5,
            students_borrowed_count=0
        )
        
        created_book = create_book(db_session, book_data)
        retrieved_book = get_book(db_session, created_book.id)
        
        assert retrieved_book is not None
        assert retrieved_book.title == "Integration Test Book"
        assert retrieved_book.author == "Test Author"
        assert retrieved_book.branch_id == branch.id

    def test_create_book_with_faculties(self, db_session):
        branch = Branch(name="Main Branch", address="123 Main St")
        faculty1 = Faculty(name="Computer Science")
        faculty2 = Faculty(name="Mathematics")
        db_session.add_all([branch, faculty1, faculty2])
        db_session.commit()
        
        book_data = BookCreate(
            title="Book with Faculties",
            author="Test Author",
            branch_id=branch.id,
            copies_available=5,
            students_borrowed_count=0,
            faculty_ids=[faculty1.id, faculty2.id]
        )
        
        created_book = create_book(db_session, book_data)
        
        assert len(created_book.faculties) == 2
        faculty_names = [faculty.name for faculty in created_book.faculties]
        assert "Computer Science" in faculty_names
        assert "Mathematics" in faculty_names

    def test_create_duplicate_book_raises_exception(self, db_session):
        branch = Branch(name="Main Branch", address="123 Main St")
        db_session.add(branch)
        db_session.commit()
        
        book_data = BookCreate(
            title="Duplicate Book",
            author="Same Author",
            branch_id=branch.id,
            copies_available=5,
            students_borrowed_count=0
        )
        
        create_book(db_session, book_data)
        
        with pytest.raises(DuplicateBookException):
            create_book(db_session, book_data)

    def test_delete_book(self, db_session):
        branch = Branch(name="Main Branch", address="123 Main St")
        db_session.add(branch)
        db_session.commit()
        
        book_data = BookCreate(
            title="Book to Delete",
            author="Test Author",
            branch_id=branch.id,
            copies_available=5,
            students_borrowed_count=0
        )
        
        created_book = create_book(db_session, book_data)
        deleted_book = delete_book(db_session, created_book.id)
        
        assert deleted_book.id == created_book.id
        assert get_book(db_session, created_book.id) is None

    def test_get_all_books(self, db_session):
        branch = Branch(name="Main Branch", address="123 Main St")
        db_session.add(branch)
        db_session.commit()
        
        book1_data = BookCreate(
            title="Book 1",
            author="Author 1",
            branch_id=branch.id,
            copies_available=5,
            students_borrowed_count=0
        )
        
        book2_data = BookCreate(
            title="Book 2",
            author="Author 2",
            branch_id=branch.id,
            copies_available=3,
            students_borrowed_count=0
        )
        
        create_book(db_session, book1_data)
        create_book(db_session, book2_data)
        
        all_books = get_books(db_session)
        
        assert len(all_books) == 2
        titles = [book.title for book in all_books]
        assert "Book 1" in titles
        assert "Book 2" in titles


class TestBranchIntegration:
    def test_create_and_get_branch(self, db_session):
        branch_data = BranchCreate(name="Test Branch", address="Test Address")
        
        created_branch = create_branch(db_session, branch_data)
        retrieved_branch = get_branch(db_session, created_branch.id)
        
        assert retrieved_branch is not None
        assert retrieved_branch.name == "Test Branch"
        assert retrieved_branch.address == "Test Address"

    def test_get_all_branches(self, db_session):
        branch1_data = BranchCreate(name="Branch 1", address="Address 1")
        branch2_data = BranchCreate(name="Branch 2", address="Address 2")
        
        create_branch(db_session, branch1_data)
        create_branch(db_session, branch2_data)
        
        all_branches = get_branches(db_session)
        
        assert len(all_branches) == 2


class TestFacultyIntegration:
    def test_create_and_get_faculties(self, db_session):
        faculty_data = FacultyCreate(name="Test Faculty")
        
        create_faculty(db_session, faculty_data)
        all_faculties = get_faculties(db_session)
        
        assert len(all_faculties) == 1
        assert all_faculties[0].name == "Test Faculty"


class TestBookQueriesIntegration:
    def test_get_book_copies_in_branch(self, db_session):
        branch = Branch(name="Main Branch", address="123 Main St")
        db_session.add(branch)
        db_session.commit()
        
        book_data = BookCreate(
            title="Test Book",
            author="Test Author",
            branch_id=branch.id,
            copies_available=7,
            students_borrowed_count=0
        )
        
        create_book(db_session, book_data)
        
        copies = get_book_copies_in_branch(db_session, "Main Branch", "Test Book")
        
        assert copies == 7

    def test_get_book_faculties_in_branch(self, db_session):
        branch = Branch(name="Main Branch", address="123 Main St")
        faculty1 = Faculty(name="Science")
        faculty2 = Faculty(name="Engineering")
        db_session.add_all([branch, faculty1, faculty2])
        db_session.commit()
        
        book_data = BookCreate(
            title="Technical Book",
            author="Tech Author",
            branch_id=branch.id,
            copies_available=5,
            students_borrowed_count=0,
            faculty_ids=[faculty1.id, faculty2.id]
        )
        
        create_book(db_session, book_data)
        
        result = get_book_faculties_in_branch(db_session, "Technical Book", "Main Branch")
        
        assert result["book_title"] == "Technical Book"
        assert result["branch_name"] == "Main Branch"
        assert result["faculties_count"] == 2
        assert "Science" in result["faculties"]
        assert "Engineering" in result["faculties"]