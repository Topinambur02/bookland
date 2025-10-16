CREATE TABLE branches (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE,
    address VARCHAR
);

CREATE TABLE faculties (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    publisher VARCHAR,
    year INTEGER,
    pages INTEGER,
    illustrations INTEGER,
    price DOUBLE PRECISION,
    branch_id INTEGER REFERENCES branches(id),
    copies_available INTEGER DEFAULT 0,
    students_borrowed_count INTEGER DEFAULT 0
);

CREATE TABLE book_faculty (
    book_id INTEGER REFERENCES books(id),
    faculty_id INTEGER REFERENCES faculties(id)
);

CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_branches_name ON branches(name);
CREATE INDEX idx_faculties_name ON faculties(name);
