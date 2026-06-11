# Default Arguments --> Provide default value.
# It's used becouse backend APIs often have optional values.


def greet(name="Guest"):

    print("Hello", name)

greet()
greet("Adyaprana")



def country(name="India"):

    print(name)

country()
country("USA")
print("---------------------------------------")



# Keyword Arguments:

def student(name, age):

    print(name)
    print(age)

student(age=23, name="Adyaprana")