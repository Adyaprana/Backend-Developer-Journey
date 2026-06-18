# WHAT IS VENV: --> This is the thing almost every beginner uses but doesn't understand.

# THE PROBLEM WITHOUT VENV

# Imagine:
# Project A needs: Flask 2.2
# Project B needs: Flask 3.0

# Your computer: Only one Flask installed
# Conflict: Project breaks.

# VENV SOLUTION: Each project gets its own Python environment.
# Example:
# Project A
#    venv/
#    Flask 2.2

# Project B
#     venv/
#     Flask 3.0
# No conflict: 

# WHAT IS INSIDE VENV?
# When you create: python -m venv env
# Python creates:
# env/
#     Scripts/
#     Lib/
#     Include/
# Contains:
# Separate Python interpreter
# Separate package storage
# Separate dependencies

# Think: Virtual Room.
# Project lives inside room.
# Packages stay inside room.
# Other projects can't disturb it.

# CREATE VENV
# Windows: python -m venv env
# Creates: env/
#              Folder.

# ACTIVATE VENV
# Windows: env\Scripts\activate
# Output: (env)
#            C:\project>

# That (env) means: You entered virtual environment.
# INSTALL PACKAGE INSIDE VENV
# pip install flask

# Flask goes only inside:
# env/
# Not system-wide.

# DEACTIVATE
# deactivate
# Leaves environment.

# Without venv:
# Package conflicts
# Broken projects
# Version problems

# With venv:
# Project isolation
# Clean setup
# Easy deployment
# Professional workflow


# REQUIREMENTS.TXT --> Save installed packages.
# pip freeze > requirements.txt

# Creates:
# Flask==3.1.0
# requests==2.32.0

# Install everything later:
# pip install -r requirements.txt

# REAL FLASK WORKFLOW
# mkdir project
# cd project
# python -m venv env
# env\Scripts\activate
# pip install flask
# pip freeze > requirements.txt

# This is the workflow you'll use in:
# Flask
# FastAPI
# Django
# Backend APIs
# Basically every Python backend project.





# INTERVIEW QUESTIONS: 
# Q1. What is a module?
# Answer: A Python file containing code.

# Q2. What is a package?
# Answer: A folder containing modules.

# Q3. Difference between module and package?
# Answer: Module = File || Package = Folder

# Q4. What does import do?
# Answer: Loads module into program.

# Q5. Difference between: import: math and from math import sqrt
# Answer: First imports entire module. Second imports only specific function.

# Q6. What is pip?
# Answer: Python Package Installer.

# Q7. What is venv?
# Answer: Virtual Environment used to isolate project dependencies.

# Q8. Why use venv?
# Answer: Avoid package version conflicts.

# Q9. How to create venv?
# Answer: python -m venv env

# Q10. How to activate venv?
# Answer: Windows: env\Scripts\activate

# Q11. How to deactivate venv?
# Answer: deactivate

# Q12. What is requirements.txt?
# Answer: File containing project dependencies.

# Q13. How to generate requirements.txt?
# Answer: pip freeze > requirements.txt

# Q14. How to install requirements.txt?
# Answer: pip install -r requirements.txt

# Q15. Why are modules important?
# Answer: They allow code reuse and organization.