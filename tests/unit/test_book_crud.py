import pytest
from unittest.mock import Mock, create_autospec
from sqlalchemy.orm import Session
from models.models import Book, Branch, Faculty
from schemas.schemas import BookCreate, BranchCreate, FacultyCreate
from exceptions.exceptions import (
    BranchNotFoundException,
    DuplicateBookException,
    FacultyNotFoundException,
    BookNotFoundException,
)
from crud.crud import (
    get_book, get_books, create_book, delete_book,
    get_branch, get_branches, create_branch,
    create_faculty, get_faculties, get_book_copies_in_branch,
    get_book_faculties_in_branch
)


class TestBookCRUD:
    def test_get_book_found(self):
        mock_db = create_autospec(Session)
        mock_book = Mock(spec=Book)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_book
        
        result = get_book(mock_db, 1)
        
        assert result == mock_book
        mock_db.query.assert_called_once_with(Book)
        mock_db.query.return_value.filter.assert_called_once()

    def test_get_book_not_found(self):
        mock_db = create_autospec(Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = get_book(mock_db, 999)
        
        assert result is None

    def test_get_books(self):
        mock_db = create_autospec(Session)
        mock_books = [Mock(spec=Book), Mock(spec=Book)]
        mock_db.query.return_value.all.return_value = mock_books
        
        result = get_books(mock_db)
        
        assert result == mock_books
        mock_db.query.assert_called_once_with(Book)

    def test_create_book_branch_not_found(self):
        mock_db = create_autospec(Session)
        book_data = BookCreate(
            title="Test Book",
            author="Test Author",
            branch_id=999,
            copies_available=5,
            students_borrowed_count=0
        )
        
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(BranchNotFoundException):
            create_book(mock_db, book_data)

    def test_create_book_duplicate(self):
        mock_db = create_autospec(Session)
        book_data = BookCreate(
            title="Test Book",
            author="Test Author",
            branch_id=1,
            copies_available=5,
            students_borrowed_count=0
        )
        
        mock_branch = Mock(spec=Branch)
        mock_existing_book = Mock(spec=Book)
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_branch,
            mock_existing_book
        ]
        
        with pytest.raises(DuplicateBookException):
            create_book(mock_db, book_data)

    def test_create_book_faculty_not_found(self):
        mock_db = create_autospec(Session)
        book_data = BookCreate(
            title="Test Book",
            author="Test Author",
            branch_id=1,
            copies_available=5,
            students_borrowed_count=0,
            faculty_ids=[1, 999]
        )
        
        mock_branch = Mock(spec=Branch)
        mock_faculties = [Mock(spec=Faculty)]
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_branch,
            None
        ]
        mock_db.query.return_value.filter.return_value.all.return_value = mock_faculties
        
        with pytest.raises(FacultyNotFoundException):
            create_book(mock_db, book_data)

    def test_delete_book_success(self):
        mock_db = create_autospec(Session)
        mock_book = Mock(spec=Book)
        
        with pytest.MonkeyPatch().context() as m:
            m.setattr('crud.crud.get_book', lambda db, book_id: mock_book)
            
            result = delete_book(mock_db, 1)
            
            assert result == mock_book
            mock_db.delete.assert_called_once_with(mock_book)
            mock_db.commit.assert_called_once()

    def test_delete_book_not_found(self):
        mock_db = create_autospec(Session)
        
        with pytest.MonkeyPatch().context() as m:
            m.setattr('crud.crud.get_book', lambda db, book_id: None)
            
            with pytest.raises(BookNotFoundException):
                delete_book(mock_db, 999)


class TestBranchCRUD:
    def test_get_branch_found(self):
        mock_db = create_autospec(Session)
        mock_branch = Mock(spec=Branch)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_branch
        
        result = get_branch(mock_db, 1)
        
        assert result == mock_branch

    def test_get_branches(self):
        mock_db = create_autospec(Session)
        mock_branches = [Mock(spec=Branch), Mock(spec=Branch)]
        mock_db.query.return_value.all.return_value = mock_branches
        
        result = get_branches(mock_db)
        
        assert result == mock_branches

    def test_create_branch(self):
        mock_db = create_autospec(Session)
        branch_data = BranchCreate(name="Test Branch", address="Test Address")
        
        result = create_branch(mock_db, branch_data)
        
        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()


class TestFacultyCRUD:
    def test_create_faculty(self):
        mock_db = create_autospec(Session)
        faculty_data = FacultyCreate(name="Test Faculty")
        
        result = create_faculty(mock_db, faculty_data)
        
        assert result is not None
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()

    def test_get_faculties(self):
        mock_db = create_autospec(Session)
        mock_faculties = [Mock(spec=Faculty), Mock(spec=Faculty)]
        mock_db.query.return_value.all.return_value = mock_faculties
        
        result = get_faculties(mock_db)
        
        assert result == mock_faculties


class TestBookQueries:
    def test_get_book_copies_in_branch_found(self):
        mock_db = create_autospec(Session)
        mock_branch = Mock(spec=Branch, id=1)
        mock_book = Mock(spec=Book, copies_available=3)
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_branch,
            mock_book
        ]
        
        result = get_book_copies_in_branch(mock_db, "Test Branch", "Test Book")
        
        assert result == 3

    def test_get_book_copies_in_branch_branch_not_found(self):
        mock_db = create_autospec(Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(BranchNotFoundException):
            get_book_copies_in_branch(mock_db, "Nonexistent Branch", "Test Book")

    def test_get_book_copies_in_branch_book_not_found(self):
        mock_db = create_autospec(Session)
        mock_branch = Mock(spec=Branch, id=1)
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_branch,
            None
        ]
        
        result = get_book_copies_in_branch(mock_db, "Test Branch", "Nonexistent Book")
        
        assert result == 0

    def test_get_book_faculties_in_branch_branch_not_found(self):
        mock_db = create_autospec(Session)
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        with pytest.raises(BranchNotFoundException):
            get_book_faculties_in_branch(mock_db, "Test Book", "Nonexistent Branch")

    def test_get_book_faculties_in_branch_book_not_found(self):
        mock_db = create_autospec(Session)
        mock_branch = Mock(spec=Branch, id=1)
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_branch,
            None
        ]
        
        with pytest.raises(BookNotFoundException):
            get_book_faculties_in_branch(mock_db, "Nonexistent Book", "Test Branch")