# THEORY 2 — WHAT IS ASYNCHRONOUS CODE?

# Imagine: You order food -> While waiting: -> Check WhatsApp, Read email, Watch YouTube
# You don't waste time, That's async.

# Python:
import asyncio
async def task1():
    print("Task 1 Started")
    await asyncio.sleep(3)
    print("Task 1 Finished")

async def task2():
    print("Task 2 Started")
    await asyncio.sleep(3)
    print("Task 2 Finished")

asyncio.run(task1())
asyncio.run(task2())
# Both can run together.
# Total: 3 seconds instead of 6.

# Async does NOT mean:
# Faster CPU

# Async means:
# Better waiting management




# THEORY 3 — WHY FASTAPI USES ASYNC
# Suppose: 1000 users request: GET /profile

# Each request:
# Talks to database
# Waits
# Gets data
# Returns response

# Most time is spent:
# WAITING
# not computing.
# FastAPI uses async to handle thousands of waiting requests efficiently.

