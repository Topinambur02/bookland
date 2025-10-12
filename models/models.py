from sqlalchemy import Column, Integer, String, Float, Table, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

book_faculty = Table(
    'book_faculty',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('faculty_id', Integer, ForeignKey('faculties.id'))
)

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String)
    year = Column(Integer)
    pages = Column(Integer)
    illustrations = Column(Integer)
    price = Column(Float)
    branch_id = Column(Integer, ForeignKey('branches.id'))
    copies_available = Column(Integer, default=0)
    students_borrowed_count = Column(Integer, default=0)
    
    branch = relationship("Branch", back_populates="books")
    faculties = relationship("Faculty", secondary=book_faculty, back_populates="books")

class Branch(Base):
    __tablename__ = "branches"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    address = Column(String)
    
    books = relationship("Book", back_populates="branch")

class Faculty(Base):
    __tablename__ = "faculties"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    books = relationship("Book", secondary=book_faculty, back_populates="faculties")