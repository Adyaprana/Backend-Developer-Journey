# f-strings — formatted strings (Modern way of printing.)
name = "Adyaprana"
age = 23

# Single quotes
# Old Method
print("My name is", name)
print("I am", age, "years old.")
# New Method using f-strings
print(f"My name is {name}")
print(f"I am {age} years old.")


# Multiple variables in a single f-string
# Old way of printing
print("My name is " + name + " and I am " + str(age) + " years old.")
# New way of printing using f-strings
print(f"My name is {name} and I am {age} years old.")



# f-strings can also include expressions
print(f"In 5 years, I will be {age + 5} years old.")
print(f"The length of my name is {len(name)} characters.")
print(f"My name in uppercase is {name.upper()}.")