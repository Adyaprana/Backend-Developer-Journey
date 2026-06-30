# THEORY 3 — GIL (Global Interpreter Lock)

# What is GIL?
# GIL stands for: Global Interpreter Lock
# It allows only one thread to execute Python bytecode at a time in the standard CPython interpreter.

# Python have GIL --> To protect memory management and keep reference counting safe.
# GIL Not always bad
# Good for: Simplicity, Memory safety.

# Bad for: CPU-bound multithreading, 

# Does GIL affect networking --> Not much.
# FastAPI, Django, Flask still scale well because they spend a lot of time waiting for network or database operations (I/O-bound work).

# Interview Question
# What is GIL?
# Answer: The Global Interpreter Lock allows only one thread to execute Python bytecode at a time in CPython.