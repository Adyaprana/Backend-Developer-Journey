# THEORY 9 — WHAT IS EVENT LOOP?
# Think: Restaurant Manager
# Manager tracks:
# Table 1 waiting
# Table 2 eating
# Table 3 paying
# instead of standing idle.

# Python Event Loop does same thing.
# It manages all async tasks.

# FULL WORKING PROGRAM:
# Async Counter

import asyncio
async def counter():
    for i in range(5):
        print(i)
        await asyncio.sleep(1)

asyncio.run(counter())

# Output:
# 0
# 1
# 2
# 3
# 4
# with 1-second delay.