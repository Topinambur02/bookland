from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.exceptions import (
    BookNotFoundException,
    BranchNotFoundException,
    FacultyNotFoundException,
    DuplicateBookException,
    InsufficientCopiesException,
    InvalidBookDataException,
)


async def book_not_found_handler(request: Request, exc: BookNotFoundException):
    return JSONResponse(status_code=404, content={"message": f"Книга не найдена: {str(exc)}"})


async def branch_not_found_handler(request: Request, exc: BranchNotFoundException):
    return JSONResponse(status_code=404, content={"message": f"Филиал не найден: {str(exc)}"})


async def faculty_not_found_handler(request: Request, exc: FacultyNotFoundException):
    return JSONResponse(status_code=404, content={"message": f"Факультет не найден: {str(exc)}"})


async def duplicate_book_handler(request: Request, exc: DuplicateBookException):
    return JSONResponse(status_code=400, content={"message": f"Дублирование книги: {str(exc)}"})


async def insufficient_copies_handler(request: Request, exc: InsufficientCopiesException):
    return JSONResponse(status_code=400, content={"message": f"Недостаточно экземпляров: {str(exc)}"})


async def invalid_book_data_handler(request: Request, exc: InvalidBookDataException):
    return JSONResponse(status_code=400, content={"message": f"Неверные данные книги: {str(exc)}"})


exception_handlers = {
    BookNotFoundException: book_not_found_handler,
    BranchNotFoundException: branch_not_found_handler,
    FacultyNotFoundException: faculty_not_found_handler,
    DuplicateBookException: duplicate_book_handler,
    InsufficientCopiesException: insufficient_copies_handler,
    InvalidBookDataException: invalid_book_data_handler,
}
