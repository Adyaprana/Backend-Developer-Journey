# WHY DECORATORS EXIST: 

# Imagine this function:
def greet():
    print("Hello")

# Now suppose every time it runs you want:
# Starting...
# Hello
# Finished...

# Without decorators:

print("Starting...")
greet()
print("Finished...")
# Again and again.


# Decorator: --> A decorator is a function that modifies or extends another function without changing its original code.

# Think: Gift + Gift Wrapper = Decorated Gift
# The gift remains the same, We just add extra functionality.