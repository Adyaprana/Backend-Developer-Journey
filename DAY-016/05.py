# Multiple Inheritance: 

# Example: 
class Father:
    def skills(self):
        print("Driving")

class Mother:
    def talent(self):
        print("Cooking")

class Child(Father, Mother):
    pass

c = Child()
c.skills()
c.talent()

# Method Resolution Order (MRO)
# Important for Multiple Inheritance.
# Tells Python's search path.

print(Child.mro())




# Why Multiple Inheritance Can Be Dangerous? 

# Sometimes:
# Father → method()
# Mother → method()

# Which method should Python call?
# This creates complexity.
# That's why companies use it carefully.

