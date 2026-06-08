# TUPLES (Similar to List but Cannot be modified. in short it is Immutable.)

# List (Can change)
# skills = ["Python","SQL"]

# Tuple (Cannot change.)
# skills = ("Python","SQL")

skills = ("Python","SQL")
print(skills[0]) # Works

# skills[0] = "Java"   #TypeError: 'tuple' object does not support item assignment



# Why Use Tuple?
# Because data should not change.
# Examples:

# Coordinates
# Database records
# Fixed configuration values
# etc.