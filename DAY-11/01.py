# What Is File I/O?
# I/O means: --> Input / Output
# File I/O means: --> Read data from file & Write data to file

# Why Do We Need Files?

# Without file: --> name = "Adyaprana"
# Program closes.
# Data lost.

# With file: --> student.txt -> Adyaprana
# Program closes.
# Data still exists.
# Permanent storage

# THEORY
# Think of variables as: RAM (Temporary Memory)
# Think of files as: Hard Disk (Permanent Memory

# open() --> Used to open files.
# Syntax: --> file = open("file.txt")

# Read() --> 
# student.txt 
# Adyaprana
# Python Backend Developer

# close()
# File should be closed after use.
# file.close()
# Good practice.

# Program: Read File 
file = open("DAY-11/student.txt")
content = file.read()
print(content)
file.close()

# Program: Writing Files
# Mode: --> w
# Means: --> Write Mode

file = open("DAY-11/student.txt","w")
file.write("Hello Python")
file.close()

# Important: w mode overwrites file, Old data removed.

file = open("DAY-11/notes.txt","w")
file.write("Day 11 Completed")
file.close()

# APPEND MODE: --> Adds data, Doesn't remove old data.
file = open("DAY-11/notes.txt","a")
file.write("\nDay 12 Planned")
file.close()

# Difference
# w → overwrite
# a → append

