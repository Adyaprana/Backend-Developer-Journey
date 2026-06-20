# Create private variable
class Student:
    def __init__(self):
        self.__age = 23  # Private

s = Student()
print(s._Student__age)  # 23 (Mangled)
print("-----------------------------------")






# Create protected variable
class Student:
    def __init__(self):
        self._age = 23  # Protected by convention

s = Student()
print(s._age)  # 23 (Accessible)
print("-----------------------------------")






# Create getter
class Student:
    def __init__(self):
        self.__age = 23
    def get_age(self):
        return self.__age

s = Student()
print(s.get_age())  # 23
print("-----------------------------------")






# Create setter
class Student:
    def __init__(self):
        self.__age = 23
    def set_age(self, age):
        self.__age = age

s = Student()
s.set_age(25)
print("-----------------------------------")






# Student class with @property
class Student:
    def __init__(self):
        self.__age = 23
    @property
    def age(self):  # Getter
        return self.__age
    @age.setter
    def age(self, value):  # Setter
        self.__age = value

s = Student()
s.age = 25  # Looks like an attribute access
print(s.age)  # 25
print("-----------------------------------")






# Employee class with salary validation
class Employee:
    def __init__(self):
        self.__salary = 0

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, value):
        if value > 0:  # Validation
            self.__salary = value

e = Employee()
e.salary = 50000
print(e.salary)  # 5000
print("-----------------------------------")






# Book class with str
class Book:
    def __init__(self, title):
        self.title = title
    def __str__(self):  # User-friendly print
        return f"Book: {self.title}"

b = Book("Python 101")
print(b)  # Book: Python 101
print("-----------------------------------")






# Shape → Circle
# Shape → Rectangle
# Polymorphic area()

class Shape:
    def area(self): 
        pass
class Circle(Shape):
    def __init__(self, r): 
        self.r = r
    def area(self): 
        return 3.14 * self.r * self.r
class Rectangle(Shape):
    def __init__(self, w, h): 
        self.w, self.h = w, h
    def area(self): 
        return self.w * self.h

# Polymorphism in action:
shapes = [Circle(2), Rectangle(3, 4)]
for s in shapes:
    print(s.area())  # Outputs: 12.56 then 12

print("-----------------------------------")






# Playlist class using len()
class Playlist:
    def __init__(self, songs):
        self.songs = songs
    def __len__(self):  # Ties into len() function
        return len(self.songs)

p = Playlist(["Song1", "Song2", "Song3"])
print(len(p))  # 3
print("-----------------------------------")






# Student equality using eq() 
class Student:
    def __init__(self, id):
        self.id = id
    def __eq__(self, other):  # Ties into == operator
        return self.id == other.id

s1 = Student(101)
s2 = Student(101)
print(s1 == s2)  # True

print("-----------------------------------")





