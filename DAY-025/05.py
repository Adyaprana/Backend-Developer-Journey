# THEORY 8 — RUNNING MULTIPLE TASKS

# Normal way:
# Task 1 → Wait
# Task 2 → Wait
# Task 3 → Wait
# Slow.

# Async way:
# Task 1
# Task 2
# Task 3
# all running together

# FULL WORKING PROGRAM:
# Multiple Simulated API Calls
import asyncio
async def api_1():
    print("API 1 Started")
    await asyncio.sleep(3)
    print("API 1 Finished")

async def api_2():
    print("API 2 Started")
    await asyncio.sleep(3)
    print("API 2 Finished")

async def api_3():
    print("API 3 Started")
    await asyncio.sleep(3)
    print("API 3 Finished")

async def main():
    await asyncio.gather(
        api_1(),
        api_2(),
        api_3()
    )

asyncio.run(main())

# Output:
# API 1 Started
# API 2 Started
# API 3 Started
# (wait 3 sec)
# API 1 Finished
# API 2 Finished
# API 3 Finished
# Total: ~3 seconds instead of 9.