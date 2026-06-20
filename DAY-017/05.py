# Dunder Methods
# Dunder means: Double Under

# Examples:
# __init__
# __str__
# __repr__
# __len__
# __eq__
# Python automatically calls them.

# str()
# Controls: print(object)

# Without str
# <class object at 0x123>

# With str
class Student:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Student({self.name})"
    
s = Student("Adyaprana")
print(s)


# With str
class Student:
    def __init__(self, name):
        self.name = name
    def str(self):
        return f"Student({self.name})"
    
s = Student("Adyaprana")
print(s)



# repr() --> Developer-friendly representation.
# Example:
class Student:
    def __repr__(self):
        return "Student Object"
    
student = Student()    
print(repr(student))  
# Used in debugging.

# Difference
# str --> Human readable.
# repr --> Developer readable.




# len() 
# Used by: len(object)
# Example:
class Playlist:
    def __init__(self, songs):
        self.songs = songs
    def __len__(self):
        return len(self.songs)

p = Playlist(["A","B","C"])
print(len(p))
# Output: 3



# eq()
# Used for equality.
# Example:
class Student:
    def __init__(self, roll):
        self.roll = roll
    def __eq__(self, other):
        return self.roll == other.roll

s1 = Student(1)
s2 = Student(1)
print(s1 == s2)

# Output: True

# Without eq: False
# because Python compares memory locations.



# EXTRA IMPORTANT TOPICS:
 
# isinstance()
# print(isinstance(circle, Shape))
# Output: True

# hasattr()
# hasattr(student, "name")
# Checks if attribute exists.

# getattr()
# getattr(student, "name")
# Gets attribute dynamically.



# INTERVIEW QUESTIONS: 

# Q1. What is Encapsulation?
# Answer: Wrapping data and methods together while restricting direct access to internal details.

# Q2. What is a private variable?
# Answer: Variable with double underscore. (self.__balance)

# Q3. What is a protected variable?
# Answer: Single underscore variable. (self._age) Convention only.

# Q4. Why use getters and setters?
# Answer: To validate and control access.

# Q5. What does @property do?
# Answer: Allows method access like an attribute.

# Q6. What is Polymorphism?
# Answer: Same method name with different behavior.

# Q7. Give a real-world example of polymorphism.
# Answer:   Animal sound:
#           Dog → Bark
#           Cat → Meow
#           Bird → Chirp

# Q8. What is Method Overriding?
# Answer: Child class providing its own implementation of parent method.

# Q9. What is str?
# Answer: Controls output of: print(object)

# Q10. Difference between str and repr?
# Answer:   str → Human readable
#           repr → Developer readable

# Q11. What is len?
# Answer: Defines behavior of: len(object)

# Q12. What is eq?
# Answer: Defines behavior of: object1 == object2

# Q13. Why are Dunder Methods important?
# Answer: They integrate custom objects with Python built-in functions and operators.

# Q14. What is Name Mangling?
# Answer: Python internally renames: __balance to _BankAccount__balance

# Q15. Why is Polymorphism useful?
# Answer: Allows writing flexible and reusable code.