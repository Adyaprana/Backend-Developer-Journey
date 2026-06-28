# DAY 25 — ASYNC/AWAIT IN PYTHON: THE COMPLETE GUIDE

> **Goal:** Understand asynchronous programming from zero — what it is, why it exists, how Python's `asyncio` works internally, and why FastAPI is built on top of it.
>
> **Week:** W4 — How the Web Works + Git + Advanced Python
>
> **Status:** ✅

---

# 🎯 Learning Roadmap

```
Async/Await in Python

  ✅ Synchronous vs Asynchronous code — core concept
  ✅ asyncio module, async def, await keyword
  ✅ Why FastAPI is async — understand this deeply
  ✅ I/O bound vs CPU bound — when to use async
  ✅ Write 3 async programs: simulated API calls with asyncio.sleep

  ▶ ArjanCodes: Async Python (English)
```

## Core Concepts Checklist

- [ ] What synchronous execution means and why it's slow for waiting tasks
- [ ] What asynchronous execution means and how it manages waiting
- [ ] What a coroutine is and how it differs from a normal function
- [ ] What the event loop is and how it schedules tasks
- [ ] The `async def` keyword — what it creates
- [ ] The `await` keyword — what it does at runtime
- [ ] `asyncio.gather()` — running tasks concurrently
- [ ] `asyncio.create_task()` — fire-and-forget tasks
- [ ] I/O Bound vs CPU Bound — the critical distinction
- [ ] Why FastAPI uses async for massive scalability
- [ ] When NOT to use async

---

# WHY THIS DAY IS IMPORTANT

You will spend your career building FastAPI applications.

Every FastAPI route can be written as:

```python
@app.get("/users")
def get_users():        # synchronous
    ...

@app.get("/users")
async def get_users():  # asynchronous
    ...
```

Most beginners write the synchronous version and have no idea what they're missing.

Without understanding async:

- You don't know why FastAPI can handle thousands of simultaneous users
- You can't use async database drivers (asyncpg, motor)
- You can't use async HTTP clients (httpx, aiohttp)
- You write blocking code that silently kills your API's performance

After today you will understand:

- Exactly what happens when you write `async def`
- Exactly what `await` does under the hood
- Why Python's event loop is so powerful
- When async helps and when it makes things worse

---

# SECTION 1 — SYNCHRONOUS CODE (THE OLD WAY)

## WHAT SYNCHRONOUS MEANS

**Synchronous** = one thing at a time, in order, no overlapping.

The word comes from Greek: *syn* (together) + *chronos* (time) = happening at the same time in sequence.

In synchronous code:

```
Task 1 starts
Task 1 finishes
Task 2 starts
Task 2 finishes
Task 3 starts
Task 3 finishes
```

Nothing else can happen while Task 1 is running. Even if Task 1 is just **waiting** for something.

---

## THE RESTAURANT ANALOGY (SYNCHRONOUS VERSION)

Imagine a waiter who:

```
1. Takes Table 1's order
2. Walks to kitchen
3. STANDS at kitchen window and WAITS for food
4. Food arrives
5. Carries food to Table 1
6. THEN goes to Table 2
7. Takes Table 2's order
8. Walks to kitchen
9. STANDS at kitchen window and WAITS again
...
```

This waiter is **synchronous**. They can only serve one table at a time. All other tables wait.

This is fine for one table. Terrible for a restaurant. Terrible for a web server handling thousands of requests.

---

## SYNCHRONOUS PYTHON CODE

```python
import time

def fetch_user_from_db():
    print("Fetching user from database...")
    time.sleep(2)   # Simulates waiting for database response
    print("User data received.")
    return {"id": 1, "name": "Adyaprana"}

def fetch_posts_from_db():
    print("Fetching posts from database...")
    time.sleep(2)   # Simulates waiting for database response
    print("Posts data received.")
    return [{"id": 1, "title": "Day 25"}]

def main():
    start = time.time()

    user  = fetch_user_from_db()    # Wait 2 seconds
    posts = fetch_posts_from_db()   # THEN wait 2 more seconds

    end = time.time()
    print(f"Total time: {end - start:.1f} seconds")  # 4.0 seconds
    print(f"User: {user['name']}, Posts: {len(posts)}")

main()
```

Output:

```
Fetching user from database...
User data received.
Fetching posts from database...
Posts data received.
Total time: 4.0 seconds
User: Adyaprana, Posts: 1
```

**Total: 4 seconds. Sequential. Wasted 2 seconds waiting while the CPU did nothing.**

This is the problem async solves.

---

## WHY SYNCHRONOUS IS SLOW FOR WEB SERVERS

A real backend server:

```
GET /profile request arrives
  → Query users table (waits 20ms for database)
  → Query settings table (waits 15ms for database)
  → Call external weather API (waits 200ms for network)
  → Format response
  → Return to client

Total wait time: ~235ms
Actual CPU computation: ~2ms
```

**97% of the time, the server is waiting. Not computing.**

In synchronous mode, while the server waits for the database, it cannot handle any other incoming requests.

With 1000 simultaneous users: 999 users are queued, waiting for the server to finish the 1 request it's currently blocked on.

This is why async matters enormously for web servers.

---

# SECTION 2 — ASYNCHRONOUS CODE (THE MODERN WAY)

## WHAT ASYNCHRONOUS MEANS

**Asynchronous** = tasks can pause and let other tasks run during the pause.

Specifically: when a task is **waiting** (for database, network, file), it steps aside and says "while I'm waiting, please run other tasks."

```
Task 1 starts
Task 1 hits a wait point → PAUSES
Task 2 starts (while Task 1 is paused)
Task 2 hits a wait point → PAUSES
Task 3 starts (while Tasks 1 and 2 are paused)
...
Task 1's wait is done → RESUMES
Task 2's wait is done → RESUMES
```

All tasks overlap their waiting. No CPU time is wasted.

---

## THE RESTAURANT ANALOGY (ASYNCHRONOUS VERSION)

A smart waiter who:

```
1. Takes Table 1's order
2. Puts order in kitchen
3. While kitchen is cooking → Takes Table 2's order
4. While kitchen is cooking → Takes Table 3's order
5. While kitchen is cooking → Checks on Table 4
6. Kitchen rings: Table 1's food ready → Delivers to Table 1
7. Kitchen rings: Table 2's food ready → Delivers to Table 2
```

This waiter is **asynchronous**. One person. Multiple tables served simultaneously. The key is that the waiter never **stands idle** waiting for the kitchen.

**Same single person. Much higher throughput.**

This is exactly what Python's asyncio does.

---

## IMPORTANT: ASYNC IS NOT MULTI-THREADING

This is the most common misconception.

```
Multi-threading:
  Multiple threads running simultaneously
  Each thread has its own CPU slice
  True parallelism (on multi-core CPUs)
  Complex to manage (race conditions, locks)

Async (asyncio):
  SINGLE thread
  SINGLE CPU core
  Tasks take turns voluntarily (cooperative multitasking)
  Simple to manage (no race conditions between tasks)
```

**Async does NOT make your CPU run faster.**

Async makes your CPU stop sitting idle during network and database waits.

```
Without async:
  CPU: [working][waiting][waiting][waiting][working][waiting]

With async:
  CPU: [working][working on task2][working on task3][working on task1]
```

The total work is the same. The idle time is eliminated.

---

# SECTION 3 — PYTHON'S asyncio MODULE

## WHAT IS asyncio?

`asyncio` is Python's built-in library for writing asynchronous code.

It was added in **Python 3.4** (2014).

The `async`/`await` keywords were added in **Python 3.5** (2015).

`asyncio` provides:

```
1. Event Loop       → The scheduler that runs async tasks
2. Coroutines       → Functions defined with async def
3. Tasks            → Coroutines wrapped to run concurrently
4. Futures          → Objects representing eventual values
5. Utilities        → asyncio.sleep, asyncio.gather, asyncio.wait, etc.
```

---

## THE EVENT LOOP — THE HEART OF asyncio

The event loop is the engine that makes everything work.

Think of it as the **restaurant manager**:

```
Event Loop Manager:
  - Knows about all pending tasks
  - Knows which tasks are waiting (for DB, network, etc.)
  - When a task starts waiting, runs another task
  - When a task's wait is over, resumes it
  - Never stops. Runs until all tasks are complete.
```

**How it works internally:**

```
Event Loop runs:

1. Run Task A until it hits an "await" point
2. Task A is now waiting → put it in "waiting" queue
3. Run Task B until it hits an "await" point
4. Task B is now waiting → put it in "waiting" queue
5. Run Task C until it hits an "await" point
6. Check: Has Task A's wait finished? YES → resume Task A
7. Task A runs until next await or completion
8. Check: Has Task B's wait finished? YES → resume Task B
... (continues until all tasks complete)
```

This is called **cooperative multitasking** because tasks voluntarily yield control at `await` points.

---

## VISUALIZING THE EVENT LOOP

```
Timeline (each column = 1 second):

             t=0    t=1    t=2    t=3
─────────────────────────────────────────
Task A       ████   WAIT   WAIT   ████
             (run)  (DB)   (DB)   (resume)

Task B              ████   WAIT   ████
                    (run)  (net)  (resume)

Task C                     ████   ████
                           (run)  (run)

Event Loop   ████   ████   ████   ████
             (A)    (B)    (C)    (A+B+C)
─────────────────────────────────────────
Total time: 3 seconds instead of 6 (if run sequentially)
```

---

# SECTION 4 — async def AND await

## async def — CREATING A COROUTINE

```python
# Normal function
def greet():
    return "Hello"

result = greet()
print(result)   # "Hello"
print(type(result))  # <class 'str'>
```

```python
# Async function (coroutine function)
async def greet():
    return "Hello"

result = greet()
print(result)   # <coroutine object greet at 0x...>
print(type(result))  # <class 'coroutine'>
```

**When you call `async def greet()`, Python does NOT run the function.**

It creates a **coroutine object** — a paused function that is ready to run when the event loop schedules it.

To actually run it:

```python
import asyncio

async def greet():
    return "Hello"

# Method 1: asyncio.run() — for top-level entry point
result = asyncio.run(greet())
print(result)  # "Hello"
```

---

## The Coroutine Life Cycle

```
async def greet():        ← defines a coroutine FUNCTION
    return "Hello"

coro = greet()            ← creates a coroutine OBJECT (not yet run)

result = asyncio.run(coro) ← runs the coroutine in an event loop
                            ← returns the final value
```

A coroutine is like a **recipe** vs. **cooking**:

```
async def greet():   → The recipe (instructions)
greet()              → Reading the recipe (nothing cooked yet)
asyncio.run(greet()) → Actually cooking (executing the instructions)
```

---

## await — PAUSING AND RESUMING

`await` can only be used **inside** an `async def` function.

`await` does two things:

```
1. PAUSES the current coroutine at this line
2. GIVES CONTROL back to the event loop to run other tasks
3. When the awaited thing finishes, RESUMES from this line
```

```python
import asyncio

async def fetch_user():
    print("Step 1: Starting database query")
    await asyncio.sleep(2)   # ← PAUSE HERE for 2 seconds
                              # ← Event loop can run other tasks now
    print("Step 2: Database query complete")
    return {"id": 1, "name": "Adyaprana"}

asyncio.run(fetch_user())
```

Output:

```
Step 1: Starting database query
(2 seconds pass — event loop could run other tasks here)
Step 2: Database query complete
```

---

## What Can You await?

You can only `await` things that are **awaitables**. There are three types:

```python
# 1. Coroutines (functions defined with async def)
await some_async_function()

# 2. Tasks (coroutines wrapped with asyncio.create_task)
task = asyncio.create_task(some_async_function())
result = await task

# 3. Futures (low-level awaitable objects)
# Usually created by asyncio internals or libraries
```

**What you CANNOT await:**

```python
# Normal synchronous functions
await time.sleep(2)        # TypeError! time.sleep is not awaitable
await requests.get(url)    # TypeError! requests.get is not awaitable
```

**Async alternatives:**

```python
# Use these instead:
await asyncio.sleep(2)     # asyncio's non-blocking sleep
await httpx.AsyncClient().get(url)  # async HTTP client
```

---

## time.sleep() vs asyncio.sleep() — Critical Difference

```python
import time
import asyncio

# time.sleep(2) — BLOCKING
# Stops the ENTIRE program for 2 seconds
# Event loop is completely frozen
# No other tasks can run
# Like a waiter STANDING at the kitchen window

# asyncio.sleep(2) — NON-BLOCKING
# SUSPENDS only the current coroutine for 2 seconds
# Event loop is FREE to run other tasks
# Like a waiter WALKING AWAY to serve other tables
# and coming back when food is ready
```

**This is the most important distinction in async programming.**

```python
# WRONG: blocks the event loop
async def bad_function():
    time.sleep(3)   # Freezes everything for 3 seconds!

# CORRECT: non-blocking
async def good_function():
    await asyncio.sleep(3)   # Only this coroutine waits
```

---

# SECTION 5 — RUNNING MULTIPLE TASKS CONCURRENTLY

## asyncio.gather() — Run Tasks in Parallel

```python
import asyncio

async def fetch_user():
    print("Fetching user...")
    await asyncio.sleep(2)
    return {"name": "Adyaprana"}

async def fetch_posts():
    print("Fetching posts...")
    await asyncio.sleep(2)
    return [{"title": "Day 25"}]

async def main():
    # gather() runs BOTH at the SAME TIME
    user, posts = await asyncio.gather(
        fetch_user(),
        fetch_posts()
    )
    print(f"User: {user['name']}, Posts: {len(posts)}")

asyncio.run(main())
```

Output:

```
Fetching user...
Fetching posts...
(only 2 seconds wait — both ran concurrently)
User: Adyaprana, Posts: 1
```

Without `gather()` (sequential):

```python
async def main_sequential():
    user  = await fetch_user()    # wait 2 seconds
    posts = await fetch_posts()   # wait 2 MORE seconds
    # Total: 4 seconds
```

With `gather()` (concurrent):

```python
async def main_concurrent():
    user, posts = await asyncio.gather(fetch_user(), fetch_posts())
    # Total: 2 seconds (both wait simultaneously)
```

**`gather()` halves the time by overlapping the waiting.**

---

## asyncio.create_task() — Fire Tasks Immediately

```python
import asyncio

async def background_job(name: str, delay: int):
    print(f"{name} started")
    await asyncio.sleep(delay)
    print(f"{name} finished after {delay}s")
    return f"{name} result"

async def main():
    # create_task() IMMEDIATELY schedules the task
    # It starts running right away (doesn't wait for you to await it)
    task1 = asyncio.create_task(background_job("Job A", 3))
    task2 = asyncio.create_task(background_job("Job B", 1))
    task3 = asyncio.create_task(background_job("Job C", 2))

    print("All tasks created. Now waiting for results...")

    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(result1, result2, result3)

asyncio.run(main())
```

Output:

```
Job A started
Job B started
Job C started
All tasks created. Now waiting for results...
Job B finished after 1s
Job C finished after 2s
Job A finished after 3s
Job A result Job B result Job C result
```

Note: All three started immediately when `create_task()` was called. They ran concurrently. Total time: 3 seconds (not 6).

---

## gather() vs create_task() — When to Use Each

```
asyncio.gather():
  → You want to run multiple coroutines and wait for ALL of them
  → You want all their results together
  → Cleaner for collecting multiple results

asyncio.create_task():
  → You want a task to start immediately in the background
  → You might not await it right away
  → Good for "fire and forget" background operations
  → Good when you want tasks running while you do other work
```

---

# SECTION 6 — I/O BOUND vs CPU BOUND

## THE MOST IMPORTANT DISTINCTION FOR ASYNC

**This determines whether async will actually help you or not.**

---

## I/O BOUND TASKS

I/O = Input/Output

I/O bound tasks spend most of their time **waiting for external resources.**

```
Waiting for:
  → Database query response        (PostgreSQL, MySQL, MongoDB)
  → HTTP API response              (REST API call, weather API)
  → File read/write               (reading CSV, writing logs)
  → Cache response                 (Redis, Memcached)
  → Message queue                  (RabbitMQ, Kafka)
  → DNS lookup
  → Email sending (SMTP)
```

Characteristics:

```
CPU usage:  LOW
Wait time:  HIGH
Async benefit: MASSIVE
```

**Example:**

```python
import asyncio

async def database_query():
    # CPU does almost nothing during this 50ms
    await asyncio.sleep(0.05)   # simulates 50ms DB query
    return [{"id": 1}, {"id": 2}]

async def api_call():
    # CPU does almost nothing during this 200ms
    await asyncio.sleep(0.2)    # simulates 200ms external API
    return {"weather": "sunny"}
```

**Async is PERFECT for these tasks.** Instead of waiting one by one, all waiting happens simultaneously.

---

## CPU BOUND TASKS

CPU bound tasks spend most of their time **making the processor compute.**

```
Heavy computation:
  → Image processing (resize, filter, convert)
  → Video encoding/decoding
  → Machine learning model training
  → Cryptography (hashing passwords with bcrypt)
  → Scientific calculations (simulations, statistics)
  → Data compression (zip, gzip)
  → Sorting huge datasets in memory
```

Characteristics:

```
CPU usage:  MAXIMUM (100%)
Wait time:  NONE
Async benefit: ZERO (or even slightly worse)
```

**Example:**

```python
# This is CPU-bound. Async does NOT help.
def heavy_calculation():
    result = 0
    for i in range(100_000_000):   # 100 million iterations
        result += i * i
    return result
```

If you put this in `async def` and run it with `asyncio.gather()`:

```python
# WRONG: async does NOT help CPU-bound work
async def heavy_calculation_wrong():
    result = 0
    for i in range(100_000_000):   # Still takes same time
        result += i * i            # No await points here
    return result                  # Never yields to event loop

async def main():
    # These do NOT run in parallel!
    # The loop runs sequentially because there are no await points
    r1, r2 = await asyncio.gather(
        heavy_calculation_wrong(),
        heavy_calculation_wrong()
    )
```

The second task cannot start until the first one finishes, because the first one NEVER gives up control (no `await` anywhere).

---

## WHAT TO USE FOR CPU-BOUND WORK

```python
# For CPU-bound tasks, use:
# 1. multiprocessing — True parallelism on multiple CPU cores
# 2. concurrent.futures.ProcessPoolExecutor — thread pool with processes
# 3. asyncio.run_in_executor() — run blocking code in a thread/process pool

import asyncio
from concurrent.futures import ProcessPoolExecutor

def heavy_cpu_task(n):
    return sum(i * i for i in range(n))

async def main():
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        # run_in_executor moves CPU work to a separate process
        result = await loop.run_in_executor(executor, heavy_cpu_task, 10_000_000)
    print(result)

asyncio.run(main())
```

---

## THE DECISION TABLE

```
┌─────────────────────────────────────────────────────────────────┐
│                      What are you doing?                        │
├──────────────────────────┬──────────────────────────────────────┤
│       I/O Bound          │          CPU Bound                   │
│  (waiting for external)  │  (heavy computation)                 │
├──────────────────────────┼──────────────────────────────────────┤
│  Database queries        │  Image processing                    │
│  HTTP API calls          │  ML model inference                  │
│  File reads/writes       │  Password hashing (bcrypt)           │
│  Redis/cache calls       │  Video encoding                      │
│  Email sending           │  Large data sorting                  │
├──────────────────────────┼──────────────────────────────────────┤
│   USE: async/await       │   USE: multiprocessing               │
│   asyncio works great    │   asyncio does NOT help              │
└──────────────────────────┴──────────────────────────────────────┘
```

**Memory trick:**

```
I/O Bound  → WAITING  → async/await fixes this
CPU Bound  → WORKING  → multiprocessing fixes this
```

---

# SECTION 7 — WHY FASTAPI USES ASYNC

## THE SCALE PROBLEM

A production API might receive:

```
10,000 requests per second
Each request hits the database: 30ms wait
Each request hits Redis cache: 5ms wait
Each request calls external API: 150ms wait

Total wait per request: ~185ms
Total compute per request: ~2ms

90% of each request's lifetime is WAITING.
```

**Synchronous FastAPI (bad approach):**

```
Request 1 arrives → Server starts processing
Server waits for DB (30ms) → Server is FROZEN
Server waits for Redis (5ms) → Server is FROZEN
Server waits for API (150ms) → Server is FROZEN
Request 1 finishes after 185ms
Request 2 can NOW start

With 10,000 requests:
  Each waits for ALL previous ones to fully complete
  Queue builds up
  Response times explode
  Server appears "slow" even though CPU is barely used
```

**Async FastAPI (correct approach):**

```
Request 1 arrives → Server starts processing
Server hits DB await → RELEASES control to event loop
Request 2 arrives → Event loop handles it immediately
Request 3 arrives → Event loop handles it immediately
...
DB response for Request 1 arrives → Event loop resumes Request 1
Redis response for Request 1 → Event loop resumes
...

All 10,000 requests are being processed concurrently
Most of them are just waiting — and their waiting OVERLAPS
The one thread handles all of them efficiently
```

---

## HOW FASTAPI IMPLEMENTS ASYNC

```python
from fastapi import FastAPI
import asyncio

app = FastAPI()

# ASYNC ROUTE — FastAPI runs this in the event loop
# Can handle thousands of concurrent requests
@app.get("/profile")
async def get_profile():
    # await means: while DB is responding, handle other requests
    user = await database.fetch_one("SELECT * FROM users WHERE id = 1")
    return user

# SYNC ROUTE — FastAPI runs this in a thread pool
# Still works, but doesn't participate in the event loop
# FastAPI automatically runs sync routes in a thread pool
# to prevent them from blocking the event loop
@app.get("/profile-sync")
def get_profile_sync():
    user = database.fetch_one_sync("SELECT * FROM users WHERE id = 1")
    return user
```

**FastAPI's smart behavior:**

```
async def route → runs directly in the event loop
def route       → FastAPI runs in a thread pool (so it doesn't block)
```

FastAPI is built on **Starlette**, which is built on **uvicorn**, which uses Python's `asyncio` event loop. The entire stack is async from bottom to top.

---

## THE UVICORN CONNECTION

When you run:

```bash
uvicorn main:app --reload
```

Uvicorn:

```
1. Creates an asyncio event loop
2. Starts listening for HTTP connections
3. For each connection → creates a coroutine to handle it
4. The event loop runs all these coroutines concurrently
5. Each coroutine can await I/O without blocking others
```

This is why FastAPI/Uvicorn can handle so many requests on a single thread.

---

## ASYNC DATABASE DRIVERS (WHAT YOU'LL USE)

For async FastAPI to actually be async end-to-end, you need async database drivers:

```python
# Sync driver (BLOCKS the event loop — avoid in FastAPI)
import psycopg2
conn = psycopg2.connect(DATABASE_URL)

# Async driver (NON-BLOCKING — use this in FastAPI)
import asyncpg
conn = await asyncpg.connect(DATABASE_URL)

# SQLAlchemy async (what most FastAPI projects use)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
engine = create_async_engine("postgresql+asyncpg://...")
```

**If you use a synchronous database driver in an async FastAPI route, you block the event loop.** All the async benefits disappear. This is a common mistake.

---

# SECTION 8 — THREE PRACTICAL ASYNC PROGRAMS

## PROGRAM 1 — Simulated API Gateway (Sequential vs Concurrent)

This program shows the exact performance difference between sequential and concurrent async calls.

```python
import asyncio
import time

# ─────────────────────────────────────────────────────────────────
# Simulated external API calls
# In production, these would use: await httpx.AsyncClient().get(url)
# ─────────────────────────────────────────────────────────────────

async def fetch_user_profile(user_id: int) -> dict:
    """Simulates a database query for user profile (50ms)."""
    print(f"  → [DB] Querying user profile for user_id={user_id}...")
    await asyncio.sleep(0.05)   # 50ms database latency
    return {
        "id": user_id,
        "name": "Adyaprana Pradhan",
        "email": "adya@example.com"
    }

async def fetch_user_orders(user_id: int) -> list:
    """Simulates fetching orders from orders service (100ms)."""
    print(f"  → [Orders Service] Fetching orders for user_id={user_id}...")
    await asyncio.sleep(0.1)    # 100ms network call to orders service
    return [
        {"id": 1, "item": "Python Book", "price": 599},
        {"id": 2, "item": "Mechanical Keyboard", "price": 3499}
    ]

async def fetch_user_recommendations(user_id: int) -> list:
    """Simulates ML recommendation service call (200ms)."""
    print(f"  → [ML Service] Fetching recommendations for user_id={user_id}...")
    await asyncio.sleep(0.2)    # 200ms ML service response
    return [
        {"product": "FastAPI Book", "score": 0.95},
        {"product": "PostgreSQL Course", "score": 0.88}
    ]

# ─────────────────────────────────────────────────────────────────
# APPROACH 1: Sequential (the wrong way for I/O bound work)
# ─────────────────────────────────────────────────────────────────

async def build_dashboard_sequential(user_id: int):
    print("\n=== SEQUENTIAL APPROACH ===")
    start = time.perf_counter()

    profile         = await fetch_user_profile(user_id)
    orders          = await fetch_user_orders(user_id)
    recommendations = await fetch_user_recommendations(user_id)

    elapsed = time.perf_counter() - start
    print(f"  ✅ Sequential total time: {elapsed:.3f}s")
    print(f"  Expected: ~0.350s (50+100+200ms)")
    return {"profile": profile, "orders": orders, "recommendations": recommendations}

# ─────────────────────────────────────────────────────────────────
# APPROACH 2: Concurrent with gather (the correct way)
# ─────────────────────────────────────────────────────────────────

async def build_dashboard_concurrent(user_id: int):
    print("\n=== CONCURRENT APPROACH ===")
    start = time.perf_counter()

    profile, orders, recommendations = await asyncio.gather(
        fetch_user_profile(user_id),
        fetch_user_orders(user_id),
        fetch_user_recommendations(user_id)
    )

    elapsed = time.perf_counter() - start
    print(f"  ✅ Concurrent total time: {elapsed:.3f}s")
    print(f"  Expected: ~0.200s (all three run simultaneously, bottleneck = 200ms)")
    return {"profile": profile, "orders": orders, "recommendations": recommendations}

async def main():
    print("Building user dashboard for user_id=42\n")
    print("Making 3 service calls:")
    print("  DB query:          50ms")
    print("  Orders service:   100ms")
    print("  ML service:       200ms")

    await build_dashboard_sequential(42)
    await build_dashboard_concurrent(42)

    print("\n📊 RESULT:")
    print("  Sequential:  ~350ms  (50 + 100 + 200)")
    print("  Concurrent:  ~200ms  (all running simultaneously)")
    print("  Speedup:     1.75x faster for this example")
    print("  Real APIs:   can be 10x+ faster with more services")

asyncio.run(main())
```

**Expected output:**

```
Building user dashboard for user_id=42

Making 3 service calls:
  DB query:          50ms
  Orders service:   100ms
  ML service:       200ms

=== SEQUENTIAL APPROACH ===
  → [DB] Querying user profile for user_id=42...
  → [Orders Service] Fetching orders for user_id=42...
  → [ML Service] Fetching recommendations for user_id=42...
  ✅ Sequential total time: 0.351s

=== CONCURRENT APPROACH ===
  → [DB] Querying user profile for user_id=42...
  → [Orders Service] Fetching orders for user_id=42...
  → [ML Service] Fetching recommendations for user_id=42...
  ✅ Concurrent total time: 0.201s

📊 RESULT:
  Sequential:  ~350ms
  Concurrent:  ~200ms
  Speedup:     1.75x faster
```

---

## PROGRAM 2 — Async Task Queue with Retry Logic

This program simulates a production pattern: multiple API calls, some fail, automatic retry.

```python
import asyncio
import random
import time

# ─────────────────────────────────────────────────────────────────
# Simulated unreliable external payment gateway
# In production: await httpx.AsyncClient().post(url, json=payload)
# ─────────────────────────────────────────────────────────────────

async def call_payment_gateway(order_id: int, amount: float) -> dict:
    """
    Simulates an external payment gateway call.
    70% success rate. 30% failure rate (real gateways have occasional failures).
    """
    print(f"  💳 [Payment Gateway] Processing order #{order_id} (₹{amount:.2f})...")
    await asyncio.sleep(0.15)   # 150ms gateway response time

    if random.random() < 0.3:   # 30% chance of failure
        raise ConnectionError(f"Payment gateway timeout for order #{order_id}")

    return {
        "order_id": order_id,
        "amount": amount,
        "status": "SUCCESS",
        "transaction_id": f"TXN{order_id:04d}{int(time.time()) % 10000}"
    }

async def process_order_with_retry(
    order_id: int,
    amount: float,
    max_retries: int = 3,
    backoff_seconds: float = 0.1
) -> dict:
    """
    Production pattern: async retry with exponential backoff.
    Tries the payment gateway up to max_retries times.
    Waits longer between each retry (exponential backoff).
    """
    for attempt in range(1, max_retries + 1):
        try:
            result = await call_payment_gateway(order_id, amount)
            if attempt > 1:
                print(f"  ✅ Order #{order_id} succeeded on attempt {attempt}")
            return result

        except ConnectionError as e:
            if attempt == max_retries:
                print(f"  ❌ Order #{order_id} FAILED after {max_retries} attempts")
                return {
                    "order_id": order_id,
                    "status": "FAILED",
                    "error": str(e)
                }

            wait_time = backoff_seconds * (2 ** (attempt - 1))   # Exponential backoff
            print(f"  ⚠️  Order #{order_id} attempt {attempt} failed. Retry in {wait_time:.2f}s...")
            await asyncio.sleep(wait_time)

async def process_all_orders(orders: list) -> list:
    """Process multiple orders concurrently."""
    print(f"\n📦 Processing {len(orders)} orders concurrently...\n")
    start = time.perf_counter()

    tasks = [
        process_order_with_retry(
            order_id=order["id"],
            amount=order["amount"]
        )
        for order in orders
    ]

    results = await asyncio.gather(*tasks, return_exceptions=False)

    elapsed = time.perf_counter() - start

    success = sum(1 for r in results if r["status"] == "SUCCESS")
    failed  = sum(1 for r in results if r["status"] == "FAILED")

    print(f"\n📊 BATCH RESULTS:")
    print(f"  Total orders:  {len(orders)}")
    print(f"  Successful:    {success}")
    print(f"  Failed:        {failed}")
    print(f"  Total time:    {elapsed:.3f}s")
    print(f"  (Sequential would take: ~{len(orders) * 0.15:.2f}s minimum)")

    return results

async def main():
    random.seed(42)   # Reproducible results for demo

    orders = [
        {"id": 1001, "amount": 599.00},
        {"id": 1002, "amount": 1299.00},
        {"id": 1003, "amount": 3499.00},
        {"id": 1004, "amount": 249.00},
        {"id": 1005, "amount": 899.00},
    ]

    results = await process_all_orders(orders)

    print("\n📋 FINAL TRANSACTION LOG:")
    for r in results:
        status_icon = "✅" if r["status"] == "SUCCESS" else "❌"
        if r["status"] == "SUCCESS":
            print(f"  {status_icon} Order #{r['order_id']} → {r['transaction_id']}")
        else:
            print(f"  {status_icon} Order #{r['order_id']} → FAILED: {r['error'][:50]}")

asyncio.run(main())
```

**Key concepts demonstrated:**

```
✅ asyncio.gather() with multiple tasks
✅ Exception handling inside async functions
✅ Exponential backoff retry pattern (used in all production systems)
✅ return_exceptions parameter in gather()
✅ Concurrent batch processing
```

---

## PROGRAM 3 — Async Pipeline (Producer → Processor → Consumer)

This simulates a real-world data pipeline pattern, like processing API responses through multiple stages.

```python
import asyncio
import time
from dataclasses import dataclass
from typing import List

# ─────────────────────────────────────────────────────────────────
# Data model
# ─────────────────────────────────────────────────────────────────

@dataclass
class RawAPIResponse:
    endpoint: str
    raw_data: dict
    fetched_at: float

@dataclass
class ProcessedRecord:
    endpoint: str
    processed_data: dict
    processing_time_ms: float

# ─────────────────────────────────────────────────────────────────
# Stage 1 — Producer: Fetch from multiple API endpoints
# ─────────────────────────────────────────────────────────────────

async def fetch_from_endpoint(endpoint: str, delay_ms: int) -> RawAPIResponse:
    """Simulates an async HTTP GET to a REST API endpoint."""
    print(f"  🌐 [Fetch] GET {endpoint} (expected: {delay_ms}ms)")
    await asyncio.sleep(delay_ms / 1000)

    # Simulated API responses based on endpoint
    mock_responses = {
        "/api/users":    {"count": 150, "users": [{"id": i, "name": f"User{i}"} for i in range(1, 6)]},
        "/api/products": {"count": 1200, "featured": ["FastAPI Book", "Redis Guide", "Docker Course"]},
        "/api/orders":   {"pending": 23, "completed": 1847, "failed": 5},
        "/api/metrics":  {"cpu": 34.2, "memory": 67.8, "requests_per_sec": 2341},
    }

    return RawAPIResponse(
        endpoint=endpoint,
        raw_data=mock_responses.get(endpoint, {"error": "unknown endpoint"}),
        fetched_at=time.perf_counter()
    )

# ─────────────────────────────────────────────────────────────────
# Stage 2 — Processor: Transform raw data
# ─────────────────────────────────────────────────────────────────

async def process_response(raw: RawAPIResponse) -> ProcessedRecord:
    """Simulates async data transformation (e.g., calling ML service, enriching data)."""
    print(f"  ⚙️  [Process] Transforming data from {raw.endpoint}...")
    await asyncio.sleep(0.02)   # 20ms processing/enrichment service

    process_start = time.perf_counter()

    # Transform the data based on endpoint
    if raw.endpoint == "/api/users":
        processed = {
            "total_users": raw.raw_data["count"],
            "sample_names": [u["name"] for u in raw.raw_data["users"]],
            "summary": f"{raw.raw_data['count']} registered users"
        }
    elif raw.endpoint == "/api/products":
        processed = {
            "catalog_size": raw.raw_data["count"],
            "featured_products": raw.raw_data["featured"],
            "summary": f"{raw.raw_data['count']} products in catalog"
        }
    elif raw.endpoint == "/api/orders":
        total = raw.raw_data["pending"] + raw.raw_data["completed"] + raw.raw_data["failed"]
        processed = {
            "total_orders": total,
            "success_rate": f"{raw.raw_data['completed']/total*100:.1f}%",
            "summary": f"{raw.raw_data['pending']} pending, {raw.raw_data['completed']} completed"
        }
    elif raw.endpoint == "/api/metrics":
        processed = {
            "health_score": "GOOD" if raw.raw_data["cpu"] < 80 else "WARNING",
            "cpu_percent": raw.raw_data["cpu"],
            "rps": raw.raw_data["requests_per_sec"],
            "summary": f"CPU: {raw.raw_data['cpu']}% | {raw.raw_data['requests_per_sec']} req/s"
        }
    else:
        processed = raw.raw_data

    processing_time = (time.perf_counter() - process_start) * 1000

    return ProcessedRecord(
        endpoint=raw.endpoint,
        processed_data=processed,
        processing_time_ms=processing_time
    )

# ─────────────────────────────────────────────────────────────────
# Stage 3 — Consumer: Save / display results
# ─────────────────────────────────────────────────────────────────

async def save_to_dashboard(records: List[ProcessedRecord]) -> None:
    """Simulates saving processed records to a dashboard store (Redis/DB)."""
    print(f"\n  💾 [Save] Writing {len(records)} records to dashboard store...")
    await asyncio.sleep(0.03)   # 30ms write to Redis/DB
    print(f"  ✅ [Save] Dashboard updated successfully.\n")

# ─────────────────────────────────────────────────────────────────
# Full Pipeline Orchestrator
# ─────────────────────────────────────────────────────────────────

async def run_dashboard_pipeline():
    """
    Full async pipeline:
    1. Fetch from 4 endpoints concurrently (Stage 1)
    2. Process all 4 responses concurrently (Stage 2)
    3. Save all records together (Stage 3)
    """
    print("🚀 Starting Dashboard Pipeline\n")
    print("=" * 50)
    pipeline_start = time.perf_counter()

    # Define endpoints and their simulated latencies (ms)
    endpoints = [
        ("/api/users",    80),
        ("/api/products", 120),
        ("/api/orders",   60),
        ("/api/metrics",  40),
    ]

    # ── Stage 1: Fetch all endpoints concurrently ──
    print("\n📡 STAGE 1: Fetching from API endpoints...")
    raw_responses: List[RawAPIResponse] = await asyncio.gather(*[
        fetch_from_endpoint(endpoint, delay)
        for endpoint, delay in endpoints
    ])
    stage1_time = time.perf_counter() - pipeline_start
    print(f"  Stage 1 complete in {stage1_time*1000:.0f}ms (bottleneck: 120ms)")

    # ── Stage 2: Process all responses concurrently ──
    print("\n🔄 STAGE 2: Processing responses...")
    processed_records: List[ProcessedRecord] = await asyncio.gather(*[
        process_response(raw)
        for raw in raw_responses
    ])
    stage2_time = (time.perf_counter() - pipeline_start) - stage1_time
    print(f"  Stage 2 complete in {stage2_time*1000:.0f}ms")

    # ── Stage 3: Save to dashboard ──
    print("\n💾 STAGE 3: Saving to dashboard...")
    await save_to_dashboard(processed_records)

    # ── Final Results ──
    total_time = time.perf_counter() - pipeline_start

    print("=" * 50)
    print("📊 DASHBOARD SUMMARY\n")
    for record in processed_records:
        print(f"  {record.endpoint}")
        print(f"    → {record.processed_data.get('summary', 'N/A')}")

    print(f"\n⏱️  PERFORMANCE:")
    print(f"  Total pipeline time:    {total_time*1000:.0f}ms")
    print(f"  Stage 1 (fetch):        {stage1_time*1000:.0f}ms")
    print(f"  Stage 2 (process):      {stage2_time*1000:.0f}ms")
    print(f"  Stage 3 (save):         ~30ms")
    print(f"\n  If sequential: ~{sum(d for _,d in endpoints) + 20*4 + 30:.0f}ms")
    print(f"  Async pipeline: ~{total_time*1000:.0f}ms")
    print(f"  Speedup: {(sum(d for _,d in endpoints) + 20*4 + 30) / (total_time*1000):.1f}x faster")

asyncio.run(run_dashboard_pipeline())
```

**Key concepts demonstrated:**

```
✅ Multi-stage async pipeline design pattern
✅ Using dataclasses with async code
✅ Type hints in async functions
✅ Measuring performance with time.perf_counter()
✅ gather() at each pipeline stage
✅ Real-world architecture: producer → processor → consumer
```

---

# SECTION 9 — ADVANCED ASYNC PATTERNS

## async with — Async Context Managers

Used for resources that need async setup and cleanup.

```python
import asyncio
import httpx   # pip install httpx

async def fetch_multiple_urls(urls: list) -> list:
    results = []

    # async with creates an async context manager
    # The HTTP session is opened asynchronously
    # and closed automatically when the block exits
    async with httpx.AsyncClient() as client:
        for url in urls:
            response = await client.get(url)
            results.append({
                "url": url,
                "status": response.status_code,
                "size": len(response.content)
            })

    return results

# In FastAPI with async database sessions:
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user(db: AsyncSession, user_id: int):
    async with db.begin():    # Async transaction context
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()
```

---

## async for — Async Iterators

Used when iterating over data that comes in asynchronously (like database cursors or streams).

```python
import asyncio

async def async_data_stream(n: int):
    """Simulates an async data stream (like a database cursor)."""
    for i in range(n):
        await asyncio.sleep(0.01)  # Simulate fetching next row
        yield {"row_id": i, "value": i * 10}

async def process_stream():
    print("Processing async data stream:")
    total = 0

    # async for iterates over an async generator
    async for record in async_data_stream(5):
        print(f"  Received: {record}")
        total += record["value"]

    print(f"Total: {total}")

asyncio.run(process_stream())
```

---

## asyncio.wait_for() — Timeout Handling

```python
import asyncio

async def slow_external_api():
    await asyncio.sleep(10)   # Simulates a slow API (10 seconds)
    return {"data": "response"}

async def main():
    try:
        # Give the API call maximum 2 seconds
        result = await asyncio.wait_for(slow_external_api(), timeout=2.0)
        print(result)

    except asyncio.TimeoutError:
        print("❌ API call timed out after 2 seconds")
        # Return cached data or error response

asyncio.run(main())
```

Always use `wait_for()` when calling external APIs. Never let an external service block your server indefinitely.

---

## asyncio.Semaphore — Rate Limiting Concurrent Requests

```python
import asyncio

async def fetch_url(session_id: int, semaphore: asyncio.Semaphore):
    async with semaphore:   # Only N tasks can be here simultaneously
        print(f"  Fetching for session {session_id}...")
        await asyncio.sleep(0.5)   # Simulates API call
        print(f"  Session {session_id} complete.")

async def main():
    # Allow maximum 3 concurrent API calls
    # (respects rate limits of external APIs)
    semaphore = asyncio.Semaphore(3)

    tasks = [fetch_url(i, semaphore) for i in range(10)]
    await asyncio.gather(*tasks)

asyncio.run(main())
```

---

# SECTION 10 — ASYNC IN FASTAPI (PRACTICAL)

## Complete Async FastAPI Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import time

app = FastAPI(title="Async FastAPI Demo")

# ─────────────────────────────────────────────────────────────────
# Simulated async database functions
# In production: use asyncpg, SQLAlchemy async, or Tortoise ORM
# ─────────────────────────────────────────────────────────────────

async def db_get_user(user_id: int) -> dict | None:
    await asyncio.sleep(0.03)   # 30ms DB query
    if user_id == 1:
        return {"id": 1, "name": "Adyaprana", "email": "adya@example.com"}
    return None

async def db_get_user_posts(user_id: int) -> list:
    await asyncio.sleep(0.05)   # 50ms DB query
    return [
        {"id": 1, "title": "Day 25: Async Python", "user_id": user_id},
        {"id": 2, "title": "Day 24: Git & GitHub", "user_id": user_id},
    ]

async def cache_get(key: str) -> dict | None:
    await asyncio.sleep(0.005)  # 5ms Redis check
    return None   # Cache miss

async def cache_set(key: str, value: dict) -> None:
    await asyncio.sleep(0.002)  # 2ms Redis write

# ─────────────────────────────────────────────────────────────────
# Routes
# ─────────────────────────────────────────────────────────────────

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """
    Fetches user from DB.
    Using async def allows FastAPI to handle other requests
    during the 30ms database wait.
    """
    # Check cache first
    cached = await cache_get(f"user:{user_id}")
    if cached:
        return {**cached, "source": "cache"}

    # Cache miss — fetch from database
    user = await db_get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Store in cache for next time
    await cache_set(f"user:{user_id}", user)
    return {**user, "source": "database"}


@app.get("/users/{user_id}/dashboard")
async def get_user_dashboard(user_id: int):
    """
    Fetches user AND posts CONCURRENTLY.
    Instead of:  30ms DB + 50ms DB = 80ms total
    We get:      max(30ms, 50ms) = 50ms total
    """
    user = await db_get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch user data and posts at the same time
    user_data, posts = await asyncio.gather(
        db_get_user(user_id),
        db_get_user_posts(user_id)
    )

    return {
        "user": user_data,
        "posts": posts,
        "post_count": len(posts)
    }


@app.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    Even while /dashboard is waiting for DB, this endpoint is handled.
    async allows concurrent request handling.
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "message": "Server is processing requests asynchronously"
    }
```

---

# SECTION 11 — COMMON ASYNC MISTAKES

## Mistake 1: Using time.sleep() in async code

```python
# WRONG — BLOCKS the entire event loop
async def bad_route():
    time.sleep(2)       # Freezes everything for 2 seconds
    return {"result": "done"}

# CORRECT
async def good_route():
    await asyncio.sleep(2)  # Only this coroutine waits
    return {"result": "done"}
```

---

## Mistake 2: Using synchronous HTTP library in async code

```python
# WRONG — requests library is synchronous
async def bad_fetch():
    response = requests.get("https://api.example.com/data")  # BLOCKS
    return response.json()

# CORRECT — use httpx or aiohttp
import httpx

async def good_fetch():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
    return response.json()
```

---

## Mistake 3: Forgetting await

```python
# WRONG — coroutine is created but never run
async def get_users():
    users = fetch_users_from_db()   # Missing await!
    # users is a coroutine object, not actual data
    return users

# CORRECT
async def get_users():
    users = await fetch_users_from_db()   # await = actually run it
    return users
```

---

## Mistake 4: Calling asyncio.run() inside an async function

```python
# WRONG — nested event loops cause errors
async def outer():
    result = asyncio.run(inner())   # Error: event loop already running!
    return result

# CORRECT — just await inside async functions
async def outer():
    result = await inner()   # Correct
    return result
```

---

## Mistake 5: Using async for CPU-bound work expecting speedup

```python
# WRONG expectation — this does NOT run in parallel
async def cpu_heavy_1():
    return sum(i**2 for i in range(10_000_000))   # no await = no yield

async def cpu_heavy_2():
    return sum(i**2 for i in range(10_000_000))   # no await = no yield

# gather() here is SEQUENTIAL, not concurrent
# because neither function ever yields to the event loop
await asyncio.gather(cpu_heavy_1(), cpu_heavy_2())

# CORRECT — use process pool for CPU work
from concurrent.futures import ProcessPoolExecutor

def cpu_heavy(n):
    return sum(i**2 for i in range(n))

async def run_cpu_work():
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        r1, r2 = await asyncio.gather(
            loop.run_in_executor(executor, cpu_heavy, 10_000_000),
            loop.run_in_executor(executor, cpu_heavy, 10_000_000)
        )
    return r1, r2
```

---

# SECTION 12 — INTERVIEW QUESTIONS (ADVANCED)

## Q1. What exactly is the Python event loop? How does it work internally?

The Python event loop is a **single-threaded scheduler** that manages the execution of coroutines and I/O callbacks. It is the runtime that makes async/await possible.

Internally, the event loop maintains several data structures:

**Ready queue** — coroutines that are ready to run right now. The loop takes the first one, runs it until it hits an `await`, then moves to the next.

**Pending futures** — coroutines that are waiting for I/O or timers. When the event the coroutine is waiting for occurs (DB responds, timer fires), the coroutine moves from pending back to the ready queue.

The loop uses OS-level mechanisms for I/O notification:
- `select()` / `poll()` / `epoll()` on Linux
- `kqueue()` on macOS
- `IOCP` on Windows

These syscalls let the OS tell Python "this file descriptor is now ready to read/write" without blocking.

The loop cycle:
1. Run all callbacks in the ready queue until each hits `await` or completes
2. Call `select()`/`epoll()` to check which I/O events fired
3. For each fired event, move the corresponding coroutine to the ready queue
4. Fire any timer callbacks whose time has come
5. Go back to step 1

**Why single-threaded is safe:** Since only one coroutine runs at a time (they cooperatively yield at `await`), there are no race conditions. The global state is only modified between `await` points.

---

## Q2. What is the difference between a thread, a process, and a coroutine?

**Process:**

A process is an independent program with its own memory space, file handles, and CPU state. Creating a process is expensive (milliseconds). Processes don't share memory directly. Communication requires IPC (inter-process communication: pipes, sockets, shared memory). Use for true parallelism on CPU-bound work across multiple cores.

**Thread:**

A thread is a lightweight execution context within a process. Multiple threads share the same memory space. Creating a thread is faster than a process but still has overhead (~100 microseconds). In Python, the GIL (Global Interpreter Lock) prevents true parallel execution of Python bytecode across threads, making threads good for I/O-bound but not CPU-bound work.

**Coroutine:**

A coroutine is a function that can pause and resume execution. It runs in a single thread. Creating a coroutine is extremely cheap (microseconds, just a function call). Coroutines cooperatively yield control at `await` points. No OS involvement, no context switching. The Python event loop schedules thousands of coroutines with minimal overhead.

**Summary for web servers:**

```
10,000 simultaneous requests:

Threads:    10,000 threads × ~8MB stack = 80GB RAM needed. Impractical.
Processes:  10,000 processes. Even more impractical.
Coroutines: 10,000 coroutines × ~1KB overhead = ~10MB total. Perfect.
```

This is why nginx, Node.js, and FastAPI can handle thousands of concurrent connections on a single thread/process.

---

## Q3. What is the Python GIL and how does it interact with asyncio?

The **GIL (Global Interpreter Lock)** is a mutex that protects Python's internal memory management (reference counting). It ensures only one thread executes Python bytecode at a time.

**How GIL affects threading:**

Two Python threads on a 4-core machine cannot execute Python code in true parallel. The GIL forces them to take turns. This makes Python threads largely useless for CPU-bound parallelism.

**How GIL interacts with asyncio:**

asyncio is completely unaffected by the GIL because asyncio uses a **single thread**. There is no concurrent Python bytecode execution in asyncio — only one coroutine runs at a time. The GIL is never contested.

**Where the GIL becomes relevant in async code:**

When you use `asyncio.run_in_executor()` with a `ThreadPoolExecutor` for blocking I/O operations, you're using threads. Most I/O operations in Python (network, file system) release the GIL while waiting for the OS to complete the operation. So threads ARE useful for I/O even with the GIL — they release it during the wait.

**The complete picture:**

```
CPU-bound work:  ProcessPoolExecutor (bypasses GIL by using processes)
I/O with libs that release GIL: ThreadPoolExecutor (threads release GIL during I/O)
Pure I/O with async drivers: asyncio (single thread, no GIL concern)
```

---

## Q4. What happens when you await inside an async for loop vs. using asyncio.gather()?

**await inside a loop (sequential):**

```python
results = []
for endpoint in endpoints:
    result = await fetch(endpoint)   # Each fetch runs sequentially
    results.append(result)
# Total time = sum of all individual fetch times
```

Each iteration starts only after the previous one completely finishes. The event loop is available for other coroutines between iterations (between awaits), but this specific task processes endpoints one by one.

**asyncio.gather() (concurrent):**

```python
results = await asyncio.gather(*[fetch(e) for e in endpoints])
# Total time = slowest individual fetch time (the bottleneck)
```

All fetch coroutines are scheduled simultaneously. They all start immediately and their waiting overlaps. Total time equals the slowest single call, not the sum.

**When to choose which:**

Use sequential `await` in loop when:
- Each task's result is needed to calculate the next task's input (data dependency)
- Rate limiting requires you to not hammer an API simultaneously
- Order of execution matters for side effects

Use `asyncio.gather()` when:
- Tasks are independent
- You want maximum throughput
- Tasks can run simultaneously without conflicts

---

## Q5. What is a "coroutine" exactly at the Python bytecode level?

At the bytecode level, when Python compiles an `async def` function, it generates a **code object** with the `CO_COROUTINE` flag set.

When you call the function, Python creates a `coroutine` object (similar to a generator object). This object wraps:

- The code object (bytecode)
- The local variables namespace
- The current instruction pointer (where execution paused)
- A reference to the current frame

The coroutine object has a `send()` method (inherited from the generator protocol). The event loop calls `coro.send(None)` to start or resume a coroutine. When the coroutine hits `await`, it internally calls `yield` (at the bytecode level), returning control to the caller (the event loop). When the awaited thing completes, the event loop calls `coro.send(result)` to resume execution with the result.

**This is why `async/await` is called "syntactic sugar over generators"** — the underlying mechanism is Python's generator protocol, just with friendlier syntax and better type-checking.

You can observe this:

```python
import asyncio, inspect

async def my_coroutine():
    await asyncio.sleep(1)
    return 42

coro = my_coroutine()
print(inspect.iscoroutine(coro))    # True
print(type(coro))                   # <class 'coroutine'>
print(coro.cr_code.co_flags & 0x100)  # CO_COROUTINE flag is set
```

---

## Q6. When should you use `asyncio.create_task()` instead of just awaiting a coroutine?

**Just awaiting a coroutine:**

```python
result = await some_coroutine()
# The coroutine runs. Only THEN does execution continue past this line.
# The coroutine does NOT start until this await is reached.
```

**`asyncio.create_task()`:**

```python
task = asyncio.create_task(some_coroutine())
# The coroutine is IMMEDIATELY scheduled to start in the background.
# Execution continues to the NEXT line right away.
# You can do other work before waiting for the task.
result = await task   # Wait for it here when you actually need the result
```

**Key difference:** `create_task()` immediately schedules the coroutine. It can start running on the next event loop iteration even before you `await` it.

**Practical use case:**

```python
async def main():
    # Start a slow background task immediately
    notification_task = asyncio.create_task(send_welcome_email(user_id))

    # Do fast work while email is being sent in background
    user = await db.get_user(user_id)
    session_token = generate_token(user)

    # Now wait for the email task to complete
    await notification_task

    return {"token": session_token}
```

Without `create_task()`, the email would start only after the DB query finishes. With `create_task()`, both happen concurrently.

---

## Q7. What is structured concurrency and why does asyncio.TaskGroup (Python 3.11+) matter?

**The problem with gather():**

If one task in `asyncio.gather()` raises an exception, the other tasks continue running in the background until they finish. If you don't `await` them, they become orphaned tasks. This can cause resource leaks and silent failures.

**Structured concurrency** ensures that all tasks created in a scope are properly finished (or cancelled) before that scope exits.

**`asyncio.TaskGroup` (Python 3.11+) implements structured concurrency:**

```python
import asyncio

async def fetch_data(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    if name == "slow":
        raise ValueError("Slow service failed!")
    return f"{name} data"

async def main():
    try:
        async with asyncio.TaskGroup() as group:
            task1 = group.create_task(fetch_data("fast", 0.1))
            task2 = group.create_task(fetch_data("slow", 0.5))
            task3 = group.create_task(fetch_data("medium", 0.3))
        # All tasks complete here, or all are cancelled if one fails

    except* ValueError as eg:
        print(f"One or more tasks failed: {eg.exceptions}")

asyncio.run(main())
```

If any task fails, `TaskGroup` **cancels all remaining tasks** in the group and raises an `ExceptionGroup`. No orphaned tasks. Clean, deterministic cleanup.

This is the **modern recommended approach** in Python 3.11+. For earlier versions, `asyncio.gather(return_exceptions=True)` is the workaround.

---

## Q8. How does FastAPI handle both `async def` and regular `def` routes?

FastAPI has two different execution paths depending on how you define your route:

**`async def` routes:**

```python
@app.get("/async-route")
async def async_route():
    await some_async_operation()
    return {"result": "data"}
```

FastAPI runs these directly in the **event loop**. The route is a coroutine that participates in the event loop. When it awaits, other requests can be handled. This is the high-performance path.

**`def` routes:**

```python
@app.get("/sync-route")
def sync_route():
    some_blocking_operation()   # blocking code
    return {"result": "data"}
```

FastAPI recognizes this is synchronous and runs it in a **thread pool** (via `run_in_executor()`). This prevents the synchronous code from blocking the event loop. Other async requests continue while this route runs in a separate thread.

**The important implication:**

If you write `async def` with synchronous blocking code:

```python
@app.get("/bad-async")
async def bad_async_route():
    time.sleep(2)          # WRONG: blocks the event loop
    requests.get(url)      # WRONG: blocks the event loop
    return {"result": "done"}
```

This is **worse** than `def` because FastAPI doesn't protect the event loop. The entire server freezes for 2 seconds.

**Rule:**

```
async def → use only with non-blocking async operations (await something)
def       → fine for blocking operations (FastAPI moves it to thread pool)
async def + blocking code → WORST of both worlds, avoid at all costs
```

---

# DAY 25 ASSIGNMENTS

✅ Run Program 1 and compare sequential vs concurrent timing yourself

✅ Run Program 2 and observe the retry with exponential backoff behavior

✅ Run Program 3 and understand the multi-stage pipeline output

✅ Explain to yourself: why does `await asyncio.sleep(2)` not block other tasks?

✅ Write a function that fetches 5 simulated "API endpoints" with gather() vs loop

✅ Try using `time.sleep()` instead of `asyncio.sleep()` and observe what breaks

✅ Add async routes to a simple FastAPI app and test with multiple concurrent requests

✅ Draw the event loop timeline for Program 1 on paper (which tasks run when)

✅ Explain I/O-bound vs CPU-bound to someone in plain language

---

# DAY 25 BACKEND DEVELOPER CHECKPOINT

If you can explain without notes:

**Core Concepts:**
✅ What synchronous means and why it wastes time for I/O work
✅ What asynchronous means — tasks overlap their waiting
✅ Why async is NOT multi-threading (single thread, cooperative)
✅ I/O Bound vs CPU Bound — the decision table
✅ When to use async vs multiprocessing

**Python asyncio:**
✅ What `async def` creates (a coroutine function, not a regular function)
✅ What a coroutine object is (a paused function ready to run)
✅ What `await` does (pause this, let others run, resume when done)
✅ What the event loop is (the scheduler that manages all coroutines)
✅ `asyncio.sleep()` vs `time.sleep()` (non-blocking vs blocking)
✅ `asyncio.gather()` — run tasks concurrently, collect results
✅ `asyncio.create_task()` — immediately schedule background task
✅ `asyncio.wait_for()` — timeout handling
✅ `asyncio.Semaphore` — rate limiting concurrent calls

**FastAPI Connection:**
✅ Why FastAPI uses async (I/O-heavy web server work)
✅ How FastAPI handles `async def` vs `def` routes differently
✅ Why using `time.sleep()` in `async def` is worse than using `def`
✅ The uvicorn → Starlette → FastAPI async stack

**Mistakes:**
✅ Never use `time.sleep()` in async code
✅ Never use `requests.get()` in async code (use `httpx`)
✅ Always `await` coroutines (forgetting await creates coroutine objects)
✅ Never `asyncio.run()` inside async functions
✅ Don't use `async def` for CPU-bound work expecting speedup

---

Tomorrow when you write your first real FastAPI endpoint with a database call, you won't just be typing:

```python
@app.get("/users")
async def get_users():
    users = await db.execute(select(User))
    return users.scalars().all()
```

You'll know:

```
async def       → this route runs in the event loop
await db.execute → this pauses this coroutine, 
                   event loop handles other requests during DB wait
When DB responds → this coroutine resumes exactly here
Other requests   → were handled during the ~30ms we were waiting
```

**That's the difference between copying async code and understanding why FastAPI can handle thousands of users on a single thread.**

---

## 🎥 Recommended Learning Video

> **✅ ArjanCodes: Async Python (English)**
>
> ArjanCodes explains async Python with clean, professional code examples.
> He covers coroutines, the event loop, and real patterns used in production.
>
> Watch it. Then come back and re-read this file.
> Pay special attention to the event loop visualization — once you
> see it animated, everything in this file clicks permanently.

---

*Day 25 Complete.* ✅
