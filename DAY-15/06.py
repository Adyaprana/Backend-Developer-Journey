# Multiple Objects: Create 3 objects from 1 class — understand how instances work

# One Class: 
class Student:
    pass

# Three Objects: 
s1 = Student()
s2 = Student()
s3 = Student()



# Example: 
class student():
    def __init__(self, name):
        self.name = name
    
s1 = student("Adyaprana")
s2 = student("ertahn")
s3 = student("weryfx")

print(s1.name)
print(s2.name)
print(s3.name)


# str(): Controls object printing.
# Without:
print(s1)
# Output: <__main__.student object at 0x000001D27EDF1610>

# With: 
class Student:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
    
s1 = Student("Adyaprana")
print(s1)



# Object Memory Concept: Every object gets its own memory.

s1 = Student("A")
s2 = Student("B")

# Changing:
s1.name = "C"

# does NOT affect:
s2.name




# INTERVIEW QUESTIONS: 

# Q1. What is OOP?
# Answer: A programming paradigm that organizes code using classes and objects.

# Q2. What is a Class?
# Answer: A blueprint for creating objects.

# Q3. What is an Object?
# Answer: An instance of a class.

# Q4. What is init()?
# Answer: Constructor method that runs automatically during object creation.

# Q5. What is self?
# Answer: Reference to the current object.

# Q6. What are Instance Variables?
# Answer: Variables unique to each object.

# Q7. What are Class Variables?
# Answer: Variables shared by all objects.

# Q8. Difference between Instance and Class Variable?
# Answer: Instance → unique || Class → shared

# Q9. What is an Instance Method?
# Answer: Method that works with object data and uses self.

# Q10. What is a Class Method?
# Answer: Method working with class-level data using cls.

# Q11. What is a Static Method?
# Answer: Utility method that uses neither self nor cls.

# Q12. Why use OOP?
# Answer: To organize, reuse, and maintain code better.

# Q13. Can one class create many objects?
# Answer: Yes. || One blueprint → many objects.

# Q14. What is a Constructor?
# Answer: Another name for init().

# Q15. What is Encapsulation? (Preview)
# Answer: Bundling data and methods together inside a class.
