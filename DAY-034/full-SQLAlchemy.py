# Book Management db

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL Connection
DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

engine = create_engine(DATABASE_URL)

Base = declarative_base()

# Book Model
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    author = Column(String(100), nullable=False)
    price = Column(Float)
    quantity = Column(Integer)

# Create Table
Base.metadata.create_all(engine)

# Create Session
Session = sessionmaker(bind=engine)
session = Session()

# Insert Books
book1 = Book(
    title="Atomic Habits",
    author="James Clear",
    price=599.0,
    quantity=10
)

book2 = Book(
    title="Clean Code",
    author="Robert C. Martin",
    price=899.0,
    quantity=5
)

session.add(book1)
session.add(book2)
session.commit()

# Read Data
print("All Books\n")

books = session.query(Book).all()

for book in books:
    print(
        book.id,
        book.title,
        book.author,
        book.price,
        book.quantity
    )

session.close()

# Find all books
books = session.query(Book).all()
for book in books:
    print(book.title)

# 2. Find one book
book = session.query(Book).filter_by(title="Atomic Habits").first()
print(book.title)
print(book.author)



# 3. Update a book
book = session.query(Book).filter_by(title="Atomic Habits").first()
book.price = 650
session.commit()


# 4. Delete a book
book = session.query(Book).filter_by(title="Clean Code").first()
session.delete(book)
session.commit()













# Student db

# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker

# DATABASE_URL = "postgresql+psycopg2://postgres:postgres123@localhost:5432/backend_journey"

# engine = create_engine(DATABASE_URL)

# Base = declarative_base()

# class Student(Base):
#     __tablename__ = "students"

#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)

# Base.metadata.create_all(engine)

# Session = sessionmaker(bind=engine)
# session = Session()

# student = Student(name="Adyaprana", age=23)

# session.add(student)
# session.commit()

# students = session.query(Student).all()

# for s in students:
#     print(s.id, s.name, s.age)

# session.close()
