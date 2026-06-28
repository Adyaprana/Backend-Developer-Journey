# THEORY 7 — WHAT IS await?
# await means: Pause here and Let other work happen first then Come back later.

# Example:
# await asyncio.sleep(3)
# This does NOT block the whole program.

# FULL WORKING PROGRAM: 
# Simulated API Call
import asyncio
async def fetch_user():
    print("Fetching User...")
    await asyncio.sleep(3)
    print("User Data Received")
asyncio.run(fetch_user())

# Output:
# Fetching User...
# (wait 3 sec)
# User Data Received