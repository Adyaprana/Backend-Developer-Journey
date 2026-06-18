# *args --> FastAPI uses similar concepts.
# *args allows a function to accept multiple positional arguments.

# Normal function:
def add(a,b):
    return a+b
print(add(5,7))
# Only two numbers.


def add(*args):
    total = 0

    for num in args:
        total += num
    return total

print(add(10,20,30))
print("--------------------------------------")

# **kwargs
# Accepts multiple keyword arguments.

def profile(**kwargs):
    print(kwargs)
profile(
    name="Adyaprana",
    city="Bangalore"
)


# Access Values
def profile(**kwargs):
    print(kwargs["name"])
profile(
    name="Adyaprana"
)