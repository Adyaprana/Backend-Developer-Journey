# Interview Questions:

# Q1. What is an ORM?
# Answer: An ORM (Object Relational Mapping) maps database tables to Python classes and rows to Python objects.

# Q2. Why use SQLAlchemy?
# Answer: It lets developers interact with databases using Python instead of writing raw SQL for most operations.

# Q3. What is declarative_base()?
# Answer: It creates the base class from which all SQLAlchemy models inherit.

# Q4. What is a Model?
# Answer: A Python class that represents a database table.

# Q5. What is __tablename__?
# Answer: It specifies the database table name for a model.

# Q6. What is a Session?
# Answer: A Session manages communication and transactions between your Python application and the database.

# Q7. What does session.add() do?
# Answer: It stages a new object to be inserted into the database.

# Q8. What does session.commit() do?
# Answer: It permanently saves the current transaction to the database.

# Q9. What happens if you don't call commit()?
# Answer: The changes are not permanently written to the database.

# Q10. How do you retrieve all rows?
# Answer: session.query(User).all()

# Q11. How do you retrieve one row?
# Answer: session.query(User).first() or filter by a condition.

# Q12. How do you update a record?
# Answer: Fetch the object, modify its attributes, then call session.commit().

# Q13. How do you delete a record?
# Answer: session.delete(user) then session.commit()

# Q14. What is a ForeignKey?
# Answer: It links one table to another and enforces referential integrity.

# Q15. What is relationship()?
# Answer: It lets SQLAlchemy navigate between related Python objects instead of manually joining tables.

# Q16. Does SQLAlchemy completely replace SQL?
# Answer: No. SQLAlchemy generates SQL for common operations, but developers may still write raw SQL for complex queries or performance tuning.

# Q17. Why is SQLAlchemy important for FastAPI?
# Answer: Because most FastAPI applications use SQLAlchemy (or a similar ORM) to communicate with relational databases like PostgreSQL.