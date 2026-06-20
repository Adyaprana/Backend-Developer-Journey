# @property Decorator --> Modern Python approach.

# Without @property
# student.get_age()
# Looks like method.

# With @property
# student.age
# Looks like attribute.

# Example: 
class Student:
    def __init__(self):
        self._age = 23
    @property
    def age(self):
        return self._age
s = Student()
print(s.age)


# Property Setter
class Student:
    def __init__(self):
        self._age = 23
    @property
    def age(self):
        return self._age
    @age.setter
    def age(self, value):
        if value > 0:
            self._age = value
s = Student()
s.age = 30
print(s.age)

# Invalid: s.age = -10 --> Rejected by validation.
