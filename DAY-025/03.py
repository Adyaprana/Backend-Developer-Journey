# THEORY 4 — I/O BOUND VS CPU BOUND

# I/O Bound -->
# Waiting for:
# Database
# APIs
# Files
# Network
# HTTP requests

# Example:
# response = requests.get(url)
# Most time: Waiting
# Async helps.


# CPU Bound -->
# Heavy calculations.

# Example:
result = 1
for i in range(100000000):
    result += i

# Most time: Computing
# Async does NOT help much.

# Use:
# Multiprocessing
# Cython
# Rust
# Native extensions

# QUICK MEMORY TRICK:
# I/O Bound = Waiting = Use Async
# CPU Bound = Calculating =Async not useful






# THEORY 5 — WHAT IS asyncio?
# Python's built-in async library.

# Provides:
import asyncio
# Used for:
# Event Loop
# Coroutines
# Async Tasks
# Scheduling



# THEORY 6 — WHAT IS async def?

# Normal Function:
def greet():
    return "Hello"

# Async Function:
async def greet():
    return "Hello"

# This creates: Coroutine not normal function.

# Example:
import asyncio
async def greet():
    print("Hello")

# Nothing runs yet.
# Need:
asyncio.run(greet())


# FULL WORKING PROGRAM: 
import asyncio
async def greet():
    print("Hello")
    await asyncio.sleep(2)
    print("Goodbye")
asyncio.run(greet())

# Output:
# Hello
# (wait 2 sec)
# Goodbye