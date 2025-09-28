from pydantic import BaseModel
from typing import List, Optional

class FacultyBase(BaseModel):
    name: str

class FacultyCreate(FacultyBase):
    pass

class Faculty(FacultyBase):
    id: int
    
    class Config:
        from_attributes = True

class BranchBase(BaseModel):
    name: str
    address: Optional[str] = None

class BranchCreate(BranchBase):
    pass

class Branch(BranchBase):
    id: int
    
    class Config:
        from_attributes = True

class BookBase(BaseModel):
    title: str
    author: str
    publisher: Optional[str] = None
    year: Optional[int] = None
    pages: Optional[int] = None
    illustrations: Optional[int] = None
    price: Optional[float] = None
    copies_available: int = 0
    students_borrowed_count: int = 0

class BookCreate(BookBase):
    branch_id: int
    faculty_ids: Optional[List[int]] = None

class BookUpdate(BookBase):
    branch_id: Optional[int] = None
    faculty_ids: Optional[List[int]] = None

class Book(BookBase):
    id: int
    branch_id: int
    faculties: List[Faculty] = []
    
    class Config:
        from_attributes = True

class BranchBooksCount(BaseModel):
    branch_name: str
    book_title: str
    copies_count: int

class BookFacultiesInfo(BaseModel):
    book_title: str
    branch_name: str
    faculties_count: int
    faculties: List[str]