class LibraryException(Exception):
    """Базовое исключение для библиотеки"""

    pass


class BookNotFoundException(LibraryException):
    """Книга не найдена"""

    pass


class BranchNotFoundException(LibraryException):
    """Филиал не найден"""

    pass


class FacultyNotFoundException(LibraryException):
    """Факультет не найден"""

    pass


class DuplicateBookException(LibraryException):
    """Дублирование книги"""

    pass


class InsufficientCopiesException(LibraryException):
    """Недостаточно экземпляров книги"""

    pass


class InvalidBookDataException(LibraryException):
    """Неверные данные книги"""

    pass
