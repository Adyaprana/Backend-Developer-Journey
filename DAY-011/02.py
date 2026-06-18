# WITH STATEMENT: --> with automatically manages resources and closes files safely.

# Old Method: 
file = open("DAY-11/notes.txt")
content = file.read()
print(content)
file.close()
# Problem: You may forget close().

# Modern Method: 
with open("DAY-11/notes.txt") as file:
    content = file.read()
    print(content)
# No close needed --> Automatically closes.

# with: --> Benefits:
#  Cleaner
#  Safer
#  Professional
#  Prevents file leaks

# Read Line By Line: 
with open("DAY-11/skills.txt") as file:
     for line in file:
        print(line)

# read() --> Entire file.
content = file.read()

# readline() --> One line.
line = file.readline()

# readlines() --> List of lines.
lines = file.readlines()

