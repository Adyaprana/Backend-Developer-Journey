# THEORY 10 — WHY FASTAPI IS FAST

# Example:
# User requests: /profile
# Backend: Wait DB, Wait Redis, Wait External API

# FastAPI:
# Don't waste time waiting, It handles other requests during waiting.
# That's why it scales well.



# INTERVIEW QUESTIONS: 

# Q1. What is asynchronous programming?
# Answer: A programming style where tasks can pause during waiting operations and allow other tasks to execute.

# Q2. Difference between synchronous and asynchronous?
# Answer:   Synchronous: One task at a time
#           Asynchronous: Tasks can overlap during waiting

# Q3. What is async def?
# Answer: Used to create coroutine functions.

# Q4. What is await?
# Answer: Pauses coroutine execution until awaited task completes.

# Q5. What is asyncio?
# Answer: Python library for asynchronous programming.

# Q6. What is a coroutine?
# Answer: A function defined using: async def

# Q7. What is an event loop?
# Answer: Component that manages async tasks.

# Q8. What is I/O Bound?
# Answer: Tasks mostly waiting on: Database, Network, Files, APIs.

# Q9. What is CPU Bound?
# Answer: Tasks mostly performing heavy calculations.

# Q10. Does async make CPU code faster?
# Answer: No -> Async helps waiting tasks, Not heavy calculations.

# Q11. Why is FastAPI asynchronous?
# Answer: To efficiently handle thousands of waiting requests.

# Q12. What does asyncio.sleep() do?
# Answer: Non-blocking sleep.
# Unlike: time.sleep()

# Q13. What is asyncio.gather()?
# Answer: Runs multiple coroutines concurrently.

# Q14. Can async improve API performance?
# Answer: Yes -> Especially for I/O-heavy workloads.

# Q15. When should you NOT use async?
# Answer: For CPU-heavy computations.

