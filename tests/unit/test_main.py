from sqlalchemy.orm import Session
import crud.crud as crud

class TestCRUD:
    def test_get_book_not_found(self, db_session: Session):
        result = crud.get_book(db_session, 999)
        assert result is None