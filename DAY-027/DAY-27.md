# DAY 27 — PYTHON INTERNALS, DATA STRUCTURES & INTERVIEW MASTERY

> **Goal:** Understand how Python works under the hood — memory, mutability, copying, *args/**kwargs, and master every OOP concept and interview question without looking at notes.
>
> **Week:** W4 — Advanced Python + Interview Preparation
>
> **Status:** ✅

---

# 🎯 DAY 27 ROADMAP

```
Today's Topics:

  ✅ Mutable vs Immutable
  ✅ Global Interpreter Lock (GIL)
  ✅ List vs Tuple vs Set vs Dictionary
  ✅ Deep Copy vs Shallow Copy
  ✅ *args and **kwargs
  ✅ OOP Concepts — explain without notes
  ✅ Python Memory Model
  ✅ == vs is  and  id()
  ✅ Truthy vs Falsy
  ✅ LEGB Rule and Namespaces
  ✅ Top Interview Questions
```

## Day 27 Final Checklist

- [ ] Explain mutable vs immutable with an example
- [ ] Explain what the GIL is in plain English
- [ ] Compare List, Tuple, Set, Dictionary in a table
- [ ] Explain shallow copy vs deep copy with code
- [ ] Write a function using *args and **kwargs
- [ ] Explain all OOP concepts from memory
- [ ] Explain `==` vs `is` without confusion
- [ ] Use `id()` to inspect Python memory
- [ ] Explain LEGB rule with an example
- [ ] List 5 Truthy and 5 Falsy values

---

# SECTION 1 — PYTHON MEMORY MODEL

## How Python Stores Everything

Before learning mutable vs immutable, you need to understand how Python stores data in memory. This is the foundation for everything in today's chapter.

When you write:

```python
x = 10
```

Python does NOT store `10` inside the variable `x`.

Instead:

```
Step 1: Python creates an INTEGER OBJECT with value 10
        (somewhere in memory — let's say at address 0x7f2a)

Step 2: Python creates a VARIABLE called x
        x does NOT contain 10
        x contains the ADDRESS 0x7f2a
        (x is a REFERENCE/POINTER to the object)

Step 3: When you use x, Python follows the address
        and finds the value 10
```

**ASCII Diagram:**

```
Variable Table          Memory (Objects)
─────────────          ─────────────────
x → 0x7f2a    ────►    [ int object: 10 ] at 0x7f2a
```

This is why Python variables are called **references**, not containers.

---

## id() — The Memory Address Tool

`id()` returns the memory address of any object.

```python
x = 10
print(id(x))
# 140234567890  (some memory address)

y = 10
print(id(y))
# 140234567890  (SAME address — Python reuses small integers!)

z = 99999
print(id(z))
# 140234599999  (different address)
```

**Key insight:** Python is smart. For small integers (-5 to 256) and short strings, Python doesn't create new objects — it reuses existing ones. This is called **Python Interning**.

---

## Python Interning

Python pre-creates objects for commonly used values and reuses them.

**Integer Interning (-5 to 256):**

```python
a = 100
b = 100
print(a is b)    # True  (same object in memory)
print(id(a) == id(b))  # True

a = 1000
b = 1000
print(a is b)    # False (different objects)
print(id(a) == id(b))  # False
```

**String Interning:**

```python
s1 = "hello"
s2 = "hello"
print(s1 is s2)   # True (Python interns simple strings)

s1 = "hello world"
s2 = "hello world"
print(s1 is s2)   # Might be False (not always interned)
```

**Why Python does this:**

```
Small integers like 0, 1, 2, -1 are used CONSTANTLY in programs.
If Python created a new object for each use, memory would fill up instantly.
Interning saves memory and speeds up comparison.
```

**Backend relevance:**

```python
# In FastAPI route handlers, status codes are often compared
# Python interns 200, 201, 400, 404, 500
# This makes status code comparisons very fast
status = 200
if status is 200:    # Works for interned integers
    pass
# But ALWAYS use == for comparisons — don't rely on interning
```

---

## == vs is — The Most Confused Concept in Python

This is asked in almost every Python interview.

```
==   compares VALUES    (what the objects contain)
is   compares IDENTITY  (whether they are the SAME object in memory)
```

```python
# Example 1: Lists
list1 = [1, 2, 3]
list2 = [1, 2, 3]

print(list1 == list2)   # True  (same VALUES)
print(list1 is list2)   # False (DIFFERENT objects in memory)

# Example 2: Same reference
list3 = list1           # list3 points to SAME object as list1
print(list3 is list1)   # True  (same memory address)
print(id(list1) == id(list3))   # True
```

**Memory diagram:**

```
list1 → 0xABCD  → [1, 2, 3]   ← different objects
list2 → 0xEFGH  → [1, 2, 3]     with same values

list3 → 0xABCD  → [1, 2, 3]   ← same object as list1
list1 → 0xABCD  ↗
```

**The None exception — always use `is` for None:**

```python
# WRONG
if result == None:
    pass

# CORRECT (PEP 8 recommendation)
if result is None:
    pass
if result is not None:
    pass
```

**Why?** Because `None` is a singleton in Python — there is only ONE None object in the entire Python runtime. Using `is` is faster and semantically correct.

---

## Reference Counting — How Python Frees Memory

Python tracks how many variables point to each object.

When the count reaches zero, Python deletes the object (garbage collection).

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))   # 2 (one for x, one for getrefcount's parameter)

y = x                        # y also points to same list
print(sys.getrefcount(x))   # 3

del y                        # Remove one reference
print(sys.getrefcount(x))   # 2

del x                        # Remove last reference
# Object [1, 2, 3] is now deleted from memory
```

**ASCII Diagram:**

```
After x = [1,2,3]:     ref_count = 1
         ┌──────────────────────┐
x ──────►│ list object [1,2,3]  │
         └──────────────────────┘

After y = x:           ref_count = 2
         ┌──────────────────────┐
x ──────►│ list object [1,2,3]  │◄────── y
         └──────────────────────┘

After del y:           ref_count = 1
         ┌──────────────────────┐
x ──────►│ list object [1,2,3]  │
         └──────────────────────┘

After del x:           ref_count = 0 → DELETED
         ┌──────────────────────┐
         │ (memory freed)       │
         └──────────────────────┘
```

---

# SECTION 2 — MUTABLE vs IMMUTABLE

## Definition

**Mutable** = can be changed after creation.
**Immutable** = cannot be changed after creation.

## Real World Analogy

```
Immutable = A printed book
  → Once printed, the content cannot change.
  → To change it, you need a NEW book.

Mutable = A whiteboard
  → You can erase and rewrite anything.
  → The board itself stays the same.
```

## Python's Mutable and Immutable Types

```
IMMUTABLE (cannot change):    MUTABLE (can change):
─────────────────────────     ─────────────────────
int                           list
float                         dict
str                           set
bool                          bytearray
tuple                         user-defined objects
frozenset
bytes
None
```

## What "Cannot Change" Means

```python
# String is IMMUTABLE
name = "Adya"
name[0] = "B"          # TypeError: 'str' object does not support item assignment

# But you CAN reassign the variable
name = "Badya"         # This is fine — you created a NEW string object
                       # The original "Adya" still exists (until garbage collected)
```

**Key insight:** Reassigning a variable is NOT the same as mutating an object.

```
"Adya" object at 0x100:   NEVER changes (immutable)
name variable:            CAN point to different objects
```

```python
# What really happens with reassignment:
name = "Adya"
print(id(name))      # 140234001

name = "Priya"       # New string object created
print(id(name))      # 140234999  (different address!)
                     # "Adya" object is still there in memory
                     # (will be deleted when refcount reaches 0)
```

## Mutation in Action

```python
# List is MUTABLE
fruits = ["apple", "mango", "banana"]
print(id(fruits))     # 140234001

fruits[0] = "grape"   # MUTATING the same object
print(id(fruits))     # 140234001  (SAME address! Same object was changed)
print(fruits)         # ['grape', 'mango', 'banana']
```

**This is the crucial difference:**

```
Immutable:  reassignment creates NEW object at NEW address
Mutable:    mutation changes SAME object at SAME address
```

## The Dangerous Consequence of Mutability

```python
# This surprises every beginner
list_a = [1, 2, 3]
list_b = list_a      # list_b points to SAME object as list_a

list_b.append(4)     # Mutating the object

print(list_a)        # [1, 2, 3, 4]  ← CHANGED! Even though we didn't touch list_a
print(list_b)        # [1, 2, 3, 4]
```

**Why?** Both variables point to the same list object in memory.

```
list_a ──┐
         ├──► [1, 2, 3]   list_b.append(4) changes THIS object
list_b ──┘
```

**Solution:** Use `.copy()` or `list()` to create an independent copy.

```python
list_a = [1, 2, 3]
list_b = list_a.copy()   # Creates a NEW list with same values

list_b.append(4)
print(list_a)    # [1, 2, 3]  ← unchanged
print(list_b)    # [1, 2, 3, 4]
```

## Why Immutable Types are Used as Dictionary Keys

Dictionaries need their keys to be **hashable**.

Hashable = can be converted to a fixed number (hash) that never changes.

Mutable objects CANNOT be hashable because their value can change.

```python
# These work as dict keys (immutable/hashable)
d = {}
d[42] = "integer"         # ✅ int
d["name"] = "string"      # ✅ str
d[(1, 2)] = "tuple"       # ✅ tuple

# This fails (mutable/unhashable)
d[[1, 2]] = "list"        # TypeError: unhashable type: 'list'
d[{"a": 1}] = "dict"      # TypeError: unhashable type: 'dict'
```

## Backend Relevance of Mutability

```python
# FastAPI — route paths are strings (immutable — safe to share)
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    pass

# Database connection settings — use tuple (immutable, safer)
DB_HOSTS = ("primary.db", "replica1.db", "replica2.db")  # can't be accidentally modified

# Request data — dict (mutable, we need to process/modify it)
user_data = {"name": "Adya", "email": "adya@example.com"}
user_data["created_at"] = "2026-06-21"  # safe to mutate

# API response — frozen after sending (behaves like immutable)
response_headers = frozenset(["Content-Type", "Authorization"])
```

## Common Beginner Mistakes with Mutability

**Mistake 1: Mutable default argument**

```python
# WRONG — the list is created ONCE and shared across all calls
def add_item(item, cart=[]):   # BUG!
    cart.append(item)
    return cart

print(add_item("apple"))   # ['apple']
print(add_item("mango"))   # ['apple', 'mango']  ← Expected ['mango']!

# CORRECT — use None as default
def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart

print(add_item("apple"))   # ['apple']
print(add_item("mango"))   # ['mango']  ← correct
```

**This is one of the most common Python interview trap questions.**

**Mistake 2: Assuming strings can be modified**

```python
greeting = "hello"
greeting[0] = "H"   # TypeError — strings are immutable
# Correct:
greeting = "H" + greeting[1:]   # Create new string
# or
greeting = greeting.capitalize()
```

**Mistake 3: Forgetting tuple can contain mutable objects**

```python
t = ([1, 2], [3, 4])   # Tuple containing lists
t[0].append(99)        # This WORKS! The list inside is mutable.
print(t)               # ([1, 2, 99], [3, 4])
# The tuple itself didn't change (still 2 elements)
# But the list object at t[0] was mutated
```

---

# SECTION 3 — GLOBAL INTERPRETER LOCK (GIL)

## Definition

The GIL (Global Interpreter Lock) is a mutex (lock) that allows only ONE thread to execute Python bytecode at a time.

## Simple Explanation

Imagine a kitchen with 5 chefs (threads) but only 1 knife (GIL).

```
Chef 1 grabs the knife → chops → puts knife down
Chef 2 grabs the knife → chops → puts knife down
Chef 3 grabs the knife → chops → puts knife down
```

Only one chef can use the knife at a time. Even though all 5 chefs are "working", only one is actually doing cutting at any moment.

This is exactly how Python threads work.

## Why Python Has the GIL

Python uses **reference counting** for memory management. Every object has a counter showing how many variables point to it.

If two threads changed the reference count of the same object simultaneously without a lock, the counter could become corrupted → memory errors → crashes.

The GIL was the simplest solution: let only one thread run Python bytecode at a time.

```
Without GIL:
Thread 1: ref_count = 2
Thread 2: ref_count = 2
Both decrement: ref_count should be 0 but might become 1 due to race condition
Object never gets freed → memory leak

With GIL:
Thread 1 holds GIL: ref_count goes from 2 to 1 → releases GIL
Thread 2 holds GIL: ref_count goes from 1 to 0 → object deleted safely
```

## The Practical Impact

```python
import threading
import time

def count_up(n):
    result = 0
    for i in range(n):
        result += i
    return result

# Single thread
start = time.time()
count_up(100_000_000)
print(f"Single thread: {time.time() - start:.2f}s")

# Two threads (you'd expect 2x faster — but NOT because of GIL)
start = time.time()
t1 = threading.Thread(target=count_up, args=(50_000_000,))
t2 = threading.Thread(target=count_up, args=(50_000_000,))
t1.start()
t2.start()
t1.join()
t2.join()
print(f"Two threads: {time.time() - start:.2f}s")
# Usually similar or SLOWER than single thread due to GIL overhead
```

**Output:**

```
Single thread: 4.20s
Two threads:   4.50s  ← Slower! GIL overhead + context switching
```

## When GIL Doesn't Matter

The GIL is released during:

```
1. I/O operations (network, file, database)
   Thread 1 waits for DB → releases GIL → Thread 2 runs
   This is why async/await and threading work well for I/O

2. Calls to C extensions that release the GIL
   NumPy, pandas release the GIL for heavy computation

3. Sleep operations
   time.sleep() releases the GIL
```

## Solutions for CPU-Bound Parallelism

```python
# Solution 1: multiprocessing (bypasses GIL — separate processes)
from multiprocessing import Pool

def heavy_work(n):
    return sum(i * i for i in range(n))

with Pool(4) as pool:
    results = pool.map(heavy_work, [10_000_000] * 4)
# 4 processes, each with its own Python interpreter and GIL
# True parallelism on 4 CPU cores

# Solution 2: Use libraries that release the GIL
import numpy as np
arr = np.array([1.0, 2.0, 3.0] * 1_000_000)
result = np.sum(arr)   # NumPy releases GIL for this computation
```

## GIL in Backend Development

```python
# FastAPI with uvicorn uses asyncio (not threads)
# GIL is not the bottleneck for async I/O

# For CPU-heavy FastAPI tasks (image processing, ML):
from fastapi import FastAPI
from concurrent.futures import ProcessPoolExecutor

app = FastAPI()
executor = ProcessPoolExecutor()

@app.post("/process-image")
async def process_image(image_data: bytes):
    loop = asyncio.get_event_loop()
    # Run CPU-heavy work in separate process (bypasses GIL)
    result = await loop.run_in_executor(executor, heavy_processing, image_data)
    return {"result": result}
```

**Summary table:**

```
Task Type      | Use              | GIL Impact
─────────────────────────────────────────────────
I/O bound      | asyncio/threads  | Minimal (GIL released during I/O)
CPU bound      | multiprocessing  | Bypassed (separate processes)
Mixed          | asyncio + ProcessPoolExecutor | Best of both
```

---

# SECTION 4 — LIST vs TUPLE vs SET vs DICTIONARY

## The Complete Comparison Table

```
Feature          | list        | tuple       | set          | dict
─────────────────────────────────────────────────────────────────────────────
Mutable?         | ✅ Yes      | ❌ No       | ✅ Yes       | ✅ Yes
Ordered?         | ✅ Yes      | ✅ Yes      | ❌ No        | ✅ Yes (3.7+)
Allows duplicates| ✅ Yes      | ✅ Yes      | ❌ No        | Keys: No, Values: Yes
Indexed?         | ✅ Yes      | ✅ Yes      | ❌ No        | By key only
Hashable?        | ❌ No       | ✅ Yes*     | ❌ No        | ❌ No
Syntax           | [1, 2, 3]   | (1, 2, 3)   | {1, 2, 3}    | {"a": 1}
Empty            | []          | ()          | set()        | {}
Memory           | More        | Less        | More         | Most
Speed (lookup)   | O(n)        | O(n)        | O(1)         | O(1)
Use case         | Collection  | Fixed data  | Unique items | Key-value pairs
```

*Tuple is hashable only if all its elements are hashable.

## Real World Analogies

```
list   → Shopping cart    (ordered, can add/remove items)
tuple  → GPS coordinates  (fixed, shouldn't change: (12.97, 77.59))
set    → Attendance list  (no duplicates, presence only)
dict   → Contact book     (name → phone number mapping)
```

## list — Ordered, Mutable, Allows Duplicates

```python
# Creating lists
fruits = ["apple", "mango", "banana", "apple"]  # duplicates allowed
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]           # different types

# Key list operations
fruits.append("grape")          # Add to end
fruits.insert(1, "kiwi")        # Insert at index 1
fruits.remove("apple")          # Remove first occurrence
popped = fruits.pop()           # Remove and return last
popped = fruits.pop(0)          # Remove and return at index 0
fruits.sort()                   # Sort in place
fruits.reverse()                # Reverse in place
copy = fruits.copy()            # Shallow copy
fruits.clear()                  # Remove all elements
idx = fruits.index("mango")     # Find index
count = fruits.count("apple")   # Count occurrences
fruits.extend(["fig", "date"])  # Add multiple elements

# Slicing
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[2:5])      # [2, 3, 4]     (index 2 to 4)
print(nums[:3])       # [0, 1, 2]     (first 3)
print(nums[-3:])      # [7, 8, 9]     (last 3)
print(nums[::2])      # [0, 2, 4, 6, 8]  (every 2nd)
print(nums[::-1])     # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]  (reversed)
```

**Time Complexity:**

```
append()       O(1)   amortized
insert()       O(n)   shifts elements
remove()       O(n)   searches first
pop() at end   O(1)
pop(i)         O(n)   shifts elements
index()        O(n)   linear search
in operator    O(n)   linear search
sort()         O(n log n)
len()          O(1)
```

**Backend use:**

```python
# FastAPI — list of users from database
users = [
    {"id": 1, "name": "Adya"},
    {"id": 2, "name": "Ravi"},
]
return users  # FastAPI serializes list to JSON array

# Collecting errors during validation
errors = []
if not username:
    errors.append("Username is required")
if len(password) < 8:
    errors.append("Password must be at least 8 characters")
if errors:
    raise HTTPException(status_code=400, detail=errors)
```

---

## tuple — Ordered, Immutable, Allows Duplicates

```python
# Creating tuples
coordinates = (12.9716, 77.5946)   # Bangalore lat, long
rgb = (255, 128, 0)                 # Color
single = (42,)                      # Single element tuple — note the comma!
single_wrong = (42)                 # This is just int 42, NOT a tuple

# Tuple unpacking (very Pythonic)
lat, lng = coordinates
print(lat)    # 12.9716
print(lng)    # 77.5946

# Swap variables using tuple unpacking
a, b = 10, 20
a, b = b, a      # Swap without temp variable!
print(a, b)      # 20 10

# Extended unpacking
first, *rest = (1, 2, 3, 4, 5)
print(first)   # 1
print(rest)    # [2, 3, 4, 5]

*init, last = (1, 2, 3, 4, 5)
print(init)    # [1, 2, 3, 4]
print(last)    # 5

# Functions returning multiple values (actually returns a tuple)
def get_min_max(numbers):
    return min(numbers), max(numbers)   # Returns tuple (min, max)

low, high = get_min_max([3, 1, 4, 1, 5, 9, 2, 6])
print(low, high)   # 1 9
```

**Why choose tuple over list:**

```
1. Safety: prevents accidental modification
2. Memory: tuples use ~30% less memory than lists
3. Speed: tuple creation is ~10x faster than list
4. Hashability: tuples can be dict keys, lists cannot
5. Intent: signals "this data should not change"
```

```python
import sys
my_list  = [1, 2, 3, 4, 5]
my_tuple = (1, 2, 3, 4, 5)

print(sys.getsizeof(my_list))    # 104 bytes
print(sys.getsizeof(my_tuple))   # 80 bytes  (less memory)
```

**Backend use:**

```python
# Database credentials — use tuple (immutable, safe)
DB_CONFIG = ("localhost", 5432, "mydb", "user", "password")

# HTTP methods allowed for a route — use tuple
ALLOWED_METHODS = ("GET", "POST", "HEAD")

# Using tuple as dict key (coordinates caching)
location_cache = {}
location_key = (12.9716, 77.5946)   # tuple key works
location_cache[location_key] = "Bangalore"
```

---

## set — Unordered, Mutable, NO Duplicates

```python
# Creating sets
tags = {"python", "fastapi", "backend"}
numbers = {1, 2, 3, 4, 5}
empty_set = set()    # NOTE: {} creates dict, not set!

# Adding/removing
tags.add("api")           # Add one element
tags.update(["docker", "aws"])  # Add multiple
tags.remove("backend")    # Remove (KeyError if not found)
tags.discard("nothing")   # Remove (no error if not found)
tags.pop()                # Remove and return random element

# Set operations (VERY useful in backend)
backend_skills = {"python", "fastapi", "postgresql", "redis"}
frontend_skills = {"javascript", "react", "python"}

# Union — all skills from both
all_skills = backend_skills | frontend_skills
all_skills = backend_skills.union(frontend_skills)
print(all_skills)    # {'python', 'fastapi', 'postgresql', 'redis', 'javascript', 'react'}

# Intersection — skills in BOTH
common = backend_skills & frontend_skills
common = backend_skills.intersection(frontend_skills)
print(common)    # {'python'}

# Difference — skills in backend but NOT frontend
unique_backend = backend_skills - frontend_skills
print(unique_backend)    # {'fastapi', 'postgresql', 'redis'}

# Symmetric difference — skills in EITHER but not BOTH
exclusive = backend_skills ^ frontend_skills
print(exclusive)    # {'fastapi', 'postgresql', 'redis', 'javascript', 'react'}

# Membership test — O(1) average!
print("python" in backend_skills)    # True (very fast)
print("java" in backend_skills)      # False (very fast)
```

**The most important set use case — removing duplicates:**

```python
# Remove duplicates from a list
user_ids = [1, 2, 3, 2, 1, 4, 3, 5, 5, 6]
unique_ids = list(set(user_ids))
print(unique_ids)    # [1, 2, 3, 4, 5, 6]  (order may vary)

# NOTE: set does not preserve order
# If order matters, use dict.fromkeys():
unique_ordered = list(dict.fromkeys(user_ids))
print(unique_ordered)    # [1, 2, 3, 4, 5, 6]  (order preserved)
```

**Time complexity:**

```
add()          O(1) average
remove()       O(1) average
in operator    O(1) average  ← This is why sets are powerful
union          O(len(s1) + len(s2))
intersection   O(min(len(s1), len(s2)))
```

**Backend use:**

```python
# Check if user has required permissions (set intersection)
required_perms = {"read_users", "write_users", "admin"}
user_perms = {"read_users", "write_users"}

if required_perms.issubset(user_perms):
    print("Access granted")
else:
    missing = required_perms - user_perms
    print(f"Missing permissions: {missing}")
    # Missing permissions: {'admin'}

# Deduplicate email list before sending newsletter
all_emails = get_all_subscriber_emails()   # might have duplicates
unique_emails = set(all_emails)            # instant deduplication
for email in unique_emails:
    send_newsletter(email)

# Check which users are online
online_users = {"user1", "user3", "user7"}
requested_users = {"user1", "user2", "user3"}
available = requested_users & online_users   # {'user1', 'user3'}
```

---

## dict — Key-Value Pairs, Ordered (Python 3.7+)

```python
# Creating dictionaries
user = {
    "id": 42,
    "name": "Adyaprana",
    "email": "adya@example.com",
    "active": True
}

# Key operations
print(user["name"])              # Adyaprana (KeyError if missing)
print(user.get("phone"))         # None (safe — no KeyError)
print(user.get("phone", "N/A"))  # N/A (default value)

user["phone"] = "9876543210"     # Add new key
user["name"] = "Adya"            # Update existing key
del user["phone"]                # Delete key

# Check membership
print("email" in user)    # True (checks keys)
print("Adya" in user)     # False (checks keys, not values)

# Iterating
for key in user:
    print(key)           # Prints keys

for key, value in user.items():
    print(f"{key}: {value}")

for value in user.values():
    print(value)

# Dictionary methods
keys   = list(user.keys())    # ['id', 'name', 'email', 'active']
values = list(user.values())  # [42, 'Adyaprana', 'adya@example.com', True]
items  = list(user.items())   # [('id', 42), ('name', 'Adyaprana'), ...]

# Update with another dict
extra = {"role": "admin", "verified": True}
user.update(extra)
print(user)

# Pop
role = user.pop("role")          # Remove and return
role = user.pop("missing", "N/A")  # Safe pop with default

# setdefault
user.setdefault("score", 0)      # Add key with default only if missing

# Copy
user_copy = user.copy()          # Shallow copy

# Clear
user.clear()   # Empty the dict
```

**Dictionary Comprehension:**

```python
# Square of numbers
squares = {x: x**2 for x in range(1, 6)}
print(squares)    # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Filter active users
all_users = {"Adya": True, "Ravi": False, "Priya": True}
active = {name: status for name, status in all_users.items() if status}
print(active)    # {'Adya': True, 'Priya': True}
```

**Time complexity:**

```
get/set/delete by key  O(1) average
in operator            O(1) average
iteration              O(n)
```

**Backend use (everywhere):**

```python
# JSON response is a dict
return {
    "user_id": user.id,
    "name": user.name,
    "email": user.email
}

# Request body (Pydantic parses to dict)
user_data = request.dict()

# HTTP headers are dicts
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "myapp",
    "user": "admin"
}
```

---

# SECTION 5 — DEEP COPY vs SHALLOW COPY

## The Problem That Makes Beginners Lose Hair

```python
original = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
copy1 = original          # NOT a copy — same object

copy1[0].append(99)
print(original)   # [[1, 2, 3, 99], [4, 5, 6], [7, 8, 9]]
# original changed too!
```

This happens because of how Python's memory model works.

## Shallow Copy

A shallow copy creates a NEW outer container but the inner objects are still SHARED.

```python
import copy

original = [[1, 2, 3], [4, 5, 6]]

# Method 1: .copy()
shallow1 = original.copy()

# Method 2: list()
shallow2 = list(original)

# Method 3: slicing
shallow3 = original[:]

# Method 4: copy.copy()
shallow4 = copy.copy(original)

# Test: modifying outer list
shallow1.append([7, 8, 9])   # Only shallow1 gets new row
print(original)    # [[1, 2, 3], [4, 5, 6]]  ← unchanged ✅

# Test: modifying inner list
shallow1[0].append(99)       # BOTH original and shallow1 are affected
print(original)    # [[1, 2, 3, 99], [4, 5, 6]]  ← CHANGED ❌
print(shallow1)    # [[1, 2, 3, 99], [4, 5, 6], [7, 8, 9]]
```

**Memory diagram:**

```
SHALLOW COPY:

original  → [  ref_to_list1,  ref_to_list2  ]
               ↓               ↓
shallow1  → [  ref_to_list1,  ref_to_list2  ]  ← different container
               ↑               ↑
            SAME OBJECTS — both point to same inner lists!

So: shallow1[0].append(99) changes the SAME list1 object
    that original[0] also points to.
```

## Deep Copy

A deep copy creates a completely independent copy — everything is new.

```python
import copy

original = [[1, 2, 3], [4, 5, 6]]
deep = copy.deepcopy(original)

deep[0].append(99)
print(original)    # [[1, 2, 3], [4, 5, 6]]        ← unchanged ✅
print(deep)        # [[1, 2, 3, 99], [4, 5, 6]]    ← changed ✅
```

**Memory diagram:**

```
DEEP COPY:

original  → [  ref_to_list1,  ref_to_list2  ]
                   ↓               ↓
              [1, 2, 3]        [4, 5, 6]

deep      → [  ref_to_list1_COPY,  ref_to_list2_COPY  ]
                     ↓                    ↓
                [1, 2, 3]           [4, 5, 6]
                (completely new objects — independent)
```

## When to Use Which

```
Assignment (=)    → Just another name for same object. Use when sharing is intended.
Shallow copy      → New container, shared contents. Use for simple flat collections.
Deep copy         → Completely independent. Use for nested structures.
```

## Complete Comparison

```python
import copy

original = {"user": {"name": "Adya", "scores": [95, 87, 92]}}

# Assignment
ref = original
ref["user"]["name"] = "Ravi"
print(original["user"]["name"])   # Ravi — original changed!

# Shallow copy
original = {"user": {"name": "Adya", "scores": [95, 87, 92]}}
shallow = original.copy()
shallow["user"]["name"] = "Ravi"
print(original["user"]["name"])   # Ravi — inner dict shared!

# Deep copy
original = {"user": {"name": "Adya", "scores": [95, 87, 92]}}
deep = copy.deepcopy(original)
deep["user"]["name"] = "Ravi"
print(original["user"]["name"])   # Adya — original protected ✅
```

## Backend Use of Copy

```python
# FastAPI — process request without modifying original
@app.post("/process")
async def process_data(data: dict):
    import copy
    working_copy = copy.deepcopy(data)   # Independent copy
    working_copy["processed"] = True
    working_copy["timestamp"] = datetime.now().isoformat()
    # Original data unchanged
    return working_copy

# Configuration per environment
import copy

BASE_CONFIG = {
    "database": {"pool_size": 10, "timeout": 30},
    "cache": {"ttl": 3600}
}

dev_config = copy.deepcopy(BASE_CONFIG)
dev_config["database"]["pool_size"] = 2   # Development needs fewer connections
# BASE_CONFIG unchanged
```

---

# SECTION 6 — *args AND **kwargs

## What Are They?

```
*args   → Lets a function accept ANY NUMBER of positional arguments
**kwargs → Lets a function accept ANY NUMBER of keyword arguments
```

The `*` and `**` are the operators. `args` and `kwargs` are just conventional names. You can use any name: `*numbers`, `**options`.

## *args — Any Number of Positional Arguments

```python
# Problem: what if you don't know how many numbers to add?
def add(a, b):
    return a + b

add(1, 2)        # Works
add(1, 2, 3)     # TypeError: takes 2 positional arguments but 3 were given

# Solution: *args
def add(*numbers):
    print(type(numbers))   # <class 'tuple'>  — args is always a TUPLE
    return sum(numbers)

print(add(1, 2))          # 3
print(add(1, 2, 3))       # 6
print(add(1, 2, 3, 4, 5)) # 15
print(add())              # 0  (empty tuple)
```

**Mixing regular and *args:**

```python
def greet(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet("Hello", "Adya", "Ravi", "Priya")
# Hello, Adya!
# Hello, Ravi!
# Hello, Priya!
```

**Rule:** `*args` must come AFTER regular arguments.

```python
def func(a, b, *args):
    print(a, b, args)

func(1, 2, 3, 4, 5)
# 1 2 (3, 4, 5)
# a=1, b=2, args=(3, 4, 5)
```

## **kwargs — Any Number of Keyword Arguments

```python
def print_user_info(**details):
    print(type(details))   # <class 'dict'>  — kwargs is always a DICT
    for key, value in details.items():
        print(f"{key}: {value}")

print_user_info(name="Adya", age=23, city="Bangalore", role="developer")
# name: Adya
# age: 23
# city: Bangalore
# role: developer
```

**Mixing everything:**

```python
def complete_function(pos1, pos2, *args, keyword_only, **kwargs):
    print(f"pos1: {pos1}")
    print(f"pos2: {pos2}")
    print(f"args: {args}")
    print(f"keyword_only: {keyword_only}")
    print(f"kwargs: {kwargs}")

complete_function(
    1, 2,                          # pos1, pos2
    3, 4, 5,                       # args
    keyword_only="required",       # keyword_only (must use keyword)
    extra1="hello", extra2="world" # kwargs
)
# pos1: 1
# pos2: 2
# args: (3, 4, 5)
# keyword_only: required
# kwargs: {'extra1': 'hello', 'extra2': 'world'}
```

**Order rule (must follow this):**

```
def func(positional, *args, keyword_only, **kwargs):
         ──────────  ────  ─────────────  ──────────
         1. Regular  2.*args 3. Keyword   4. **kwargs
                              only (after *)
```

## Unpacking with * and **

```python
# * unpacks a list/tuple into positional arguments
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
print(add(*numbers))    # 6  (same as add(1, 2, 3))

# ** unpacks a dict into keyword arguments
def greet(name, greeting):
    print(f"{greeting}, {name}!")

params = {"name": "Adya", "greeting": "Hello"}
greet(**params)    # Hello, Adya!
```

## Real Project Examples

**Example 1: Flexible API response builder**

```python
def build_api_response(status: str, message: str, **data):
    """
    Build a standardized API response with any additional data fields.
    Used throughout a FastAPI application.
    """
    response = {
        "status": status,
        "message": message,
        **data        # Unpack any additional fields
    }
    return response

# Usage
print(build_api_response("success", "User created", user_id=42, name="Adya"))
# {'status': 'success', 'message': 'User created', 'user_id': 42, 'name': 'Adya'}

print(build_api_response("error", "Validation failed", errors=["Name required"]))
# {'status': 'error', 'message': 'Validation failed', 'errors': ['Name required']}
```

**Example 2: Logging decorator with *args and **kwargs**

```python
import functools
import time

def log_execution(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):    # Accept ANY arguments
        print(f"▶ Calling: {func.__name__}")
        print(f"  args: {args}")
        print(f"  kwargs: {kwargs}")
        start = time.perf_counter()
        result = func(*args, **kwargs)   # Pass them through
        elapsed = time.perf_counter() - start
        print(f"✅ {func.__name__} completed in {elapsed:.4f}s")
        return result
    return wrapper

@log_execution
def create_user(name: str, email: str, role: str = "user") -> dict:
    # Simulates database insertion
    return {"id": 42, "name": name, "email": email, "role": role}

result = create_user("Adya", "adya@example.com", role="admin")
print(result)

# Output:
# ▶ Calling: create_user
#   args: ('Adya', 'adya@example.com')
#   kwargs: {'role': 'admin'}
# ✅ create_user completed in 0.0001s
# {'id': 42, 'name': 'Adya', 'email': 'adya@example.com', 'role': 'admin'}
```

**Example 3: Database query builder**

```python
def query_users(*filters, **conditions):
    """
    Build a dynamic database query.
    *filters = SQL conditions as strings
    **conditions = field=value pairs
    """
    query = "SELECT * FROM users"
    parts = list(filters)

    for field, value in conditions.items():
        parts.append(f"{field} = '{value}'")

    if parts:
        query += " WHERE " + " AND ".join(parts)

    return query

print(query_users("active = TRUE", role="admin"))
# SELECT * FROM users WHERE active = TRUE AND role = 'admin'

print(query_users(role="user", city="Bangalore"))
# SELECT * FROM users WHERE role = 'user' AND city = 'Bangalore'

print(query_users())
# SELECT * FROM users
```

## Common Mistakes with *args and **kwargs

```python
# Mistake 1: Wrong order
def wrong(a, **kwargs, *args):    # SyntaxError!
    pass

# Mistake 2: Forgetting that args is a tuple (not a list)
def func(*args):
    args.append(4)    # AttributeError: 'tuple' has no attribute 'append'
    # Fix: args = list(args)  or  args = (*args, 4)

# Mistake 3: Using same name twice
func(1, 2, x=3, x=4)    # SyntaxError: keyword argument repeated

# Mistake 4: Passing dict without **
def greet(name, greeting):
    pass
params = {"name": "Adya", "greeting": "Hi"}
greet(params)     # TypeError — params is one argument, not two
greet(**params)   # Correct
```

---

# SECTION 7 — OOP CONCEPTS (COMPLETE REVISION)

## Class and Object — The Blueprint Analogy

```
Class  = Blueprint/Template (architectural drawing of a house)
Object = Instance (actual house built from the blueprint)

One blueprint → many houses
One class      → many objects
```

```python
class User:
    # Class variable (shared by all instances)
    user_count = 0

    # Constructor — called when object is created
    def __init__(self, name: str, email: str, role: str = "user"):
        # Instance variables (unique to each object)
        self.name  = name
        self.email = email
        self.role  = role
        User.user_count += 1

    # Instance method
    def greet(self) -> str:
        return f"Hello, I'm {self.name} ({self.role})"

    # String representation
    def __str__(self) -> str:
        return f"User({self.name}, {self.email})"

    def __repr__(self) -> str:
        return f"User(name={self.name!r}, email={self.email!r}, role={self.role!r})"

    # Class method — works with the class, not instances
    @classmethod
    def get_user_count(cls) -> int:
        return cls.user_count

    # Static method — doesn't need class or instance
    @staticmethod
    def validate_email(email: str) -> bool:
        return "@" in email and "." in email.split("@")[1]

# Creating objects
user1 = User("Adyaprana", "adya@example.com", "admin")
user2 = User("Ravi",      "ravi@example.com")
user3 = User("Priya",     "priya@example.com", "moderator")

print(user1.greet())              # Hello, I'm Adyaprana (admin)
print(user2.greet())              # Hello, I'm Ravi (user)
print(str(user1))                 # User(Adyaprana, adya@example.com)
print(User.get_user_count())      # 3
print(User.validate_email("adya@example.com"))  # True
print(User.validate_email("invalid"))            # False
```

## Inheritance — Extending Behavior

```
Parent Class  = General blueprint
Child Class   = Specialized blueprint that inherits from parent

Child gets ALL parent's methods and attributes.
Child can ADD new methods.
Child can OVERRIDE parent's methods.
```

```python
class Animal:
    def __init__(self, name: str, species: str):
        self.name    = name
        self.species = species
        self.alive   = True

    def eat(self) -> str:
        return f"{self.name} is eating."

    def breathe(self) -> str:
        return f"{self.name} is breathing."

    def __str__(self) -> str:
        return f"{self.species}: {self.name}"

class Dog(Animal):
    def __init__(self, name: str, breed: str):
        super().__init__(name, "Dog")   # Call parent's __init__
        self.breed = breed

    # Override parent method
    def breathe(self) -> str:
        return f"{self.name} is panting and breathing."

    # New method (Dog-specific)
    def fetch(self) -> str:
        return f"{self.name} fetches the ball! 🎾"

class Cat(Animal):
    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name, "Cat")
        self.indoor = indoor

    def purr(self) -> str:
        return f"{self.name} purrs... 😺"

dog = Dog("Buddy", "Labrador")
cat = Cat("Whiskers")

print(dog.eat())      # Buddy is eating.         (inherited from Animal)
print(dog.breathe())  # Buddy is panting...      (overridden)
print(dog.fetch())    # Buddy fetches the ball!  (Dog-specific)
print(cat.purr())     # Whiskers purrs...

# isinstance checks
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True (Dog is a type of Animal)
print(isinstance(cat, Dog))     # False
```

## Encapsulation — Hiding Internal Details

```
Think: ATM machine
  You use buttons (public interface)
  You don't see the internal mechanisms (private internals)
  The bank protects its internal logic
```

```python
class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner            = owner          # Public
        self._account_number  = "AC" + str(id(self))[:8]  # Protected (convention)
        self.__balance        = initial_balance  # Private (name mangled)
        self.__transactions   = []

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.__balance += amount
        self.__transactions.append(f"+{amount}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        self.__transactions.append(f"-{amount}")

    @property
    def balance(self) -> float:
        """Read-only property for balance."""
        return self.__balance

    @property
    def statement(self) -> list:
        return self.__transactions.copy()   # Return copy, not original

account = BankAccount("Adyaprana", 5000)
account.deposit(2000)
account.withdraw(1000)
print(account.balance)        # 6000 (read-only)
print(account.statement)      # ['+2000', '-1000']
# account.__balance = 99999   # This creates a NEW attribute, doesn't change private!
# print(account.__balance)    # AttributeError — name mangled to _BankAccount__balance
```

**Name mangling:**

```python
# __balance becomes _BankAccount__balance internally
print(account._BankAccount__balance)   # 6000 (accessible but a bad practice)
```

## Polymorphism — Same Interface, Different Behavior

```
"Poly" = many, "morph" = forms
Same method name, different behavior in different classes
```

```python
from abc import ABC, abstractmethod
import math

class Shape(ABC):
    """Abstract base class — cannot be instantiated directly."""

    @abstractmethod
    def area(self) -> float:
        """Every shape MUST implement area()."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"

class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a = a
        self.b = b
        self.c = c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2   # Semi-perimeter
        return math.sqrt(s * (s-self.a) * (s-self.b) * (s-self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c

# Polymorphism in action — same code works for all shapes
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]

for shape in shapes:
    print(shape.describe())   # Each calls its OWN area() and perimeter()

# Output:
# Circle: area=78.54, perimeter=31.42
# Rectangle: area=24.00, perimeter=20.00
# Triangle: area=6.00, perimeter=12.00
```

## Abstraction — Hiding Complexity

```
Think: driving a car
  You use steering wheel, pedals, gear (simple interface)
  You don't need to know how the engine combustion works (hidden complexity)
```

```python
from abc import ABC, abstractmethod

class DatabaseDriver(ABC):
    """Abstract database interface — hides implementation details."""

    @abstractmethod
    def connect(self, connection_string: str) -> None:
        pass

    @abstractmethod
    def execute(self, query: str) -> list:
        pass

    @abstractmethod
    def close(self) -> None:
        pass

class PostgreSQLDriver(DatabaseDriver):
    def connect(self, connection_string: str) -> None:
        print(f"Connecting to PostgreSQL: {connection_string}")

    def execute(self, query: str) -> list:
        print(f"PostgreSQL executing: {query}")
        return [{"id": 1, "name": "Adya"}]   # Simulated result

    def close(self) -> None:
        print("PostgreSQL connection closed.")

class MongoDBDriver(DatabaseDriver):
    def connect(self, connection_string: str) -> None:
        print(f"Connecting to MongoDB: {connection_string}")

    def execute(self, query: str) -> list:
        print(f"MongoDB executing: {query}")
        return [{"_id": "abc123", "name": "Adya"}]

    def close(self) -> None:
        print("MongoDB connection closed.")

# Your application code doesn't care WHICH database is used
def fetch_users(db: DatabaseDriver) -> list:
    db.connect("db://localhost/myapp")
    users = db.execute("SELECT * FROM users")
    db.close()
    return users

# Swap databases without changing application code
pg_users = fetch_users(PostgreSQLDriver())
mg_users = fetch_users(MongoDBDriver())
```

---

# SECTION 8 — TRUTHY vs FALSY VALUES

## Definition

In Python, every value has a boolean meaning.

**Falsy values** evaluate to `False` in boolean context.

**Truthy values** evaluate to `True` in boolean context.

## All Falsy Values in Python

```python
# These are ALL the falsy values in Python:

bool(False)     # False — the boolean False itself
bool(0)         # False — integer zero
bool(0.0)       # False — float zero
bool(0j)        # False — complex zero
bool("")        # False — empty string
bool([])        # False — empty list
bool(())        # False — empty tuple
bool({})        # False — empty dict
bool(set())     # False — empty set
bool(None)      # False — None

# Everything else is TRUTHY
bool(1)         # True
bool(-1)        # True (any non-zero integer)
bool("hello")   # True (non-empty string)
bool(" ")       # True (space is non-empty!)
bool([0])       # True (list with one element)
bool([False])   # True (list is not empty)
```

## Practical Use in Backend Development

```python
# WITHOUT knowing truthy/falsy (verbose):
if len(users) > 0:
    process_users(users)
if name != "" and name is not None:
    print(name)
if data != {} and data is not None:
    save_data(data)

# WITH truthy/falsy (Pythonic — preferred):
if users:           # Empty list is falsy
    process_users(users)
if name:            # Empty string and None are falsy
    print(name)
if data:            # Empty dict is falsy
    save_data(data)

# FastAPI — checking optional parameters
@app.get("/users")
async def get_users(role: str = None, city: str = None):
    query = {}
    if role:    # Only filter if role was provided and not empty
        query["role"] = role
    if city:
        query["city"] = city
    return fetch_users(**query)
```

## Common Trap with Truthy/Falsy

```python
# Trap 1: 0 is falsy but valid data
def set_quantity(quantity):
    # WRONG — rejects valid quantity of 0
    if not quantity:
        quantity = 10   # BUG: 0 gets replaced with 10
    return quantity

# CORRECT
def set_quantity(quantity):
    if quantity is None:   # Explicit None check
        quantity = 10
    return quantity

# Trap 2: Empty list vs None
def get_items():
    return []   # Returns empty list

items = get_items()
if not items:
    print("No items")   # Prints "No items" for BOTH None and []
                        # Use 'if items is None' to distinguish

# Trap 3: Counting falsy values
scores = [0, 85, 0, 92, 0, 78]
non_zero = [s for s in scores if s]    # WRONG: removes valid 0 scores
all_valid = [s for s in scores if s is not None]  # CORRECT
```

---

# SECTION 9 — NAMESPACE AND LEGB RULE

## What is a Namespace?

A **namespace** is a container that holds variable names and their values.

Think of namespaces like different rooms in a building:

```
Building = Python program
Room 1   = Local namespace (inside a function)
Room 2   = Enclosing namespace (outer function)
Room 3   = Global namespace (module level)
Room 4   = Built-in namespace (Python's own functions)
```

## The LEGB Rule

Python looks up variable names in this exact order:

```
L → Local      (inside the current function)
E → Enclosing  (inside the outer function, for nested functions)
G → Global     (module level)
B → Built-in   (Python built-ins: len, print, range, etc.)
```

**Python stops at the FIRST place it finds the name.**

```python
# LEGB Rule in action

x = "GLOBAL"    # Global

def outer():
    x = "ENCLOSING"    # Enclosing

    def inner():
        x = "LOCAL"    # Local
        print(x)       # LOCAL  (found in L — stops here)

    inner()
    print(x)           # ENCLOSING  (L not found in outer, uses E)

outer()
print(x)           # GLOBAL  (L and E not applicable here)

# Built-in example
print(len([1, 2, 3]))   # 3  (len found in B — Built-in)
```

## global and nonlocal Keywords

```python
# Modify global variable from inside a function
counter = 0

def increment():
    global counter          # Tell Python: use the GLOBAL counter
    counter += 1

increment()
increment()
print(counter)   # 2

# Without global:
def bad_increment():
    counter += 1    # UnboundLocalError: local variable 'counter' referenced before assignment
                    # Python sees += and thinks counter is LOCAL but it's not defined locally

# nonlocal — modify enclosing function's variable
def outer():
    count = 0

    def inner():
        nonlocal count     # Use outer's count
        count += 1
        print(f"Inner count: {count}")

    inner()
    inner()
    print(f"Outer count: {count}")   # 2

outer()
```

## Backend Relevance

```python
# Global configuration (module level = Global namespace)
DATABASE_URL = "postgresql://localhost/myapp"
DEBUG = False
SECRET_KEY = "super-secret"

# These are accessible from all functions in the module
def get_db_connection():
    return connect(DATABASE_URL)   # Uses global DATABASE_URL

# Best practice: avoid modifying globals in functions
# Use return values and parameters instead
```

---

# SECTION 10 — pass, del, None

## pass — The Placeholder

`pass` is a no-operation statement. It does nothing.

```python
# Use case 1: Empty function/class stub during development
def implement_later():
    pass   # TODO: implement this

class EmptyClass:
    pass

# Use case 2: Empty if/for/while block
for item in items:
    if some_condition:
        pass   # Handle later
    else:
        process(item)

# Use case 3: Empty exception handler (not recommended but valid)
try:
    risky_operation()
except SomeError:
    pass   # Silently ignore (use carefully — hides bugs)
```

## del — Remove a Reference

```python
x = 10
del x         # Removes the variable name
# print(x)    # NameError: name 'x' is not defined

# Delete from a list
fruits = ["apple", "mango", "banana"]
del fruits[1]        # Delete at index 1
print(fruits)        # ['apple', 'banana']

del fruits[0:2]      # Delete a slice
print(fruits)        # []

# Delete from a dict
user = {"name": "Adya", "email": "adya@example.com", "password": "secret"}
del user["password"]   # Remove sensitive data before logging
print(user)            # {'name': 'Adya', 'email': 'adya@example.com'}

# Delete an object attribute
class Car:
    def __init__(self):
        self.color = "red"
        self.temp_data = "temporary"

car = Car()
del car.temp_data   # Remove attribute
```

## None — Python's Null

`None` is Python's null/nothing value.

```python
# None is a singleton — only ONE None exists
x = None
y = None
print(x is y)    # True — same object!

# Always compare with is, not ==
if result is None:
    print("No result")
if result is not None:
    print("Got result")

# Common uses
def search_user(user_id):
    # Return None if not found (instead of raising exception)
    if user_id not in database:
        return None
    return database[user_id]

result = search_user(42)
if result is None:
    print("User not found")
else:
    print(f"Found: {result['name']}")

# Optional parameters
def create_user(name: str, email: str, bio: str = None):
    user = {"name": name, "email": email}
    if bio is not None:
        user["bio"] = bio
    return user
```

---

# SECTION 11 — HASHABILITY AND FROZENSET

## What is Hashability?

A **hash** is a fixed-size integer that uniquely represents an object.

If an object can be hashed → **hashable** → can be used as a dict key or set element.

```python
# Check hashability
print(hash(42))           # Some integer
print(hash("hello"))      # Some integer
print(hash((1, 2, 3)))   # Some integer (tuples are hashable if contents are)

hash([1, 2, 3])           # TypeError: unhashable type: 'list'
hash({"a": 1})            # TypeError: unhashable type: 'dict'
```

**Rule:** Mutable objects cannot be hashed (their hash would change if mutated).

## frozenset — Immutable Set

```python
# Regular set (mutable, not hashable)
regular = {1, 2, 3}

# frozenset (immutable, hashable)
frozen = frozenset([1, 2, 3])

# Can be used as dict key
mapping = {frozen: "set of 1,2,3"}
print(mapping[frozenset([1, 2, 3])])   # "set of 1,2,3"

# All set operations work
frozen2 = frozenset([3, 4, 5])
print(frozen | frozen2)     # frozenset({1, 2, 3, 4, 5})
print(frozen & frozen2)     # frozenset({3})
```

---

# SECTION 12 — TIME COMPLEXITY OF DATA STRUCTURES

## The Big O Cheat Sheet for Python

```
OPERATION              list    tuple   set     dict
─────────────────────────────────────────────────────────
Access by index        O(1)    O(1)    N/A     N/A
Access by key          N/A     N/A     N/A     O(1)
Search (in)            O(n)    O(n)    O(1)    O(1)
Insert at end          O(1)*   N/A     O(1)    O(1)
Insert at beginning    O(n)    N/A     O(1)    O(1)
Delete                 O(n)    N/A     O(1)    O(1)
Length (len)           O(1)    O(1)    O(1)    O(1)
Iteration              O(n)    O(n)    O(n)    O(n)

* O(1) amortized for list append
```

**Practical impact:**

```python
# Finding if an item exists:
items = list(range(1_000_000))
item_set = set(range(1_000_000))

# List search — O(n) — checks each element
999_999 in items       # Slow for large lists

# Set search — O(1) — hash lookup
999_999 in item_set    # Instant regardless of size
```

```python
import time

n = 1_000_000
items = list(range(n))
item_set = set(range(n))

start = time.perf_counter()
_ = 999_999 in items
print(f"List search: {time.perf_counter() - start:.6f}s")

start = time.perf_counter()
_ = 999_999 in item_set
print(f"Set search:  {time.perf_counter() - start:.6f}s")

# Output:
# List search: 0.014s
# Set search:  0.000000s  (essentially instant)
```

---

# SECTION 13 — PYTHONIC CODE AND BEST PRACTICES

## What is Pythonic Code?

"Pythonic" means writing Python code the way Python is designed to be written — clean, readable, idiomatic.

```python
# NOT Pythonic (C-style)
i = 0
while i < len(fruits):
    print(fruits[i])
    i += 1

# Pythonic
for fruit in fruits:
    print(fruit)
```

## The Zen of Python (PEP 20)

```python
import this

# Key principles:
# Beautiful is better than ugly
# Explicit is better than implicit
# Simple is better than complex
# Readability counts
# There should be one obvious way to do it
# If the implementation is hard to explain, it's a bad idea
```

## Pythonic Patterns

```python
# 1. List comprehension instead of loops
squares = [x**2 for x in range(10)]         # Pythonic
evens   = [x for x in range(20) if x%2==0] # With condition

# 2. Dictionary comprehension
user_map = {user["id"]: user for user in users_list}

# 3. Enumerate instead of range(len())
for index, value in enumerate(fruits):
    print(f"{index}: {value}")

# 4. zip to iterate multiple lists together
names  = ["Adya", "Ravi", "Priya"]
scores = [95, 87, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# 5. Walrus operator := (Python 3.8+)
import re
text = "Phone: 9876543210"
if match := re.search(r"\d{10}", text):
    print(f"Found: {match.group()}")   # Found: 9876543210

# 6. f-strings (not .format() or %)
name = "Adya"
score = 95.5
print(f"Name: {name}, Score: {score:.1f}")   # Name: Adya, Score: 95.5

# 7. Context managers
with open("data.txt", "r") as f:
    content = f.read()   # File auto-closed after block

# 8. Unpacking
first, *rest = [1, 2, 3, 4, 5]
a, b, c = "ABC"   # String unpacking
x, y = y, x       # Swap without temp

# 9. get() for safe dict access
user = {"name": "Adya"}
email = user.get("email", "unknown@example.com")   # Safe, no KeyError

# 10. any() and all()
permissions = ["read", "write", "execute"]
has_write  = any(p == "write" for p in permissions)    # True
has_all    = all(p in permissions for p in ["read"])   # True
```

---

# SECTION 14 — TOP 50 INTERVIEW QUESTIONS

## Core Python Concepts

**Q1. What is the difference between mutable and immutable types?**

Mutable types (list, dict, set) can be modified after creation. Immutable types (int, str, tuple) cannot be modified. When you "change" an immutable value, Python creates a new object. This matters for memory efficiency, hashability, and function argument behavior (immutable args cannot be accidentally modified by a function).

**Q2. What is the GIL and how does it affect multi-threading?**

The GIL (Global Interpreter Lock) is a mutex in CPython that allows only one thread to execute Python bytecode at a time. This prevents true parallel execution of Python threads on multi-core CPUs. Threading is still useful for I/O-bound tasks (where threads release the GIL during I/O). For CPU-bound tasks, use `multiprocessing` to bypass the GIL.

**Q3. What is the difference between `==` and `is`?**

`==` compares values (calls `__eq__`). `is` compares object identity (memory address, uses `id()`). Always use `==` for value comparison and `is` only for singletons like `None`, `True`, `False`.

**Q4. What happens when you use a mutable object as a default argument?**

```python
def f(x, data=[]):
    data.append(x)
    return data
```

The list is created ONCE when the function is defined, not each call. Repeated calls share the same list, causing unexpected behavior. Fix: use `None` as default and create a new list inside the function.

**Q5. What is the difference between `deepcopy` and `copy`?**

`copy.copy()` (shallow copy) creates a new container but inner objects are still shared. `copy.deepcopy()` creates a completely independent copy including all nested objects. Use deepcopy when you need complete isolation.

**Q6. Explain *args and **kwargs.**

`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dict. They allow functions to accept a flexible number of arguments. Both are essential for writing decorators and wrapper functions.

**Q7. What is Python's LEGB rule?**

Python resolves names in this order: Local → Enclosing → Global → Built-in. Python stops at the first match. Use `global` to modify a global from a function. Use `nonlocal` to modify an enclosing function's variable.

**Q8. What is a decorator?**

A decorator is a function that takes a function as input and returns a new function, adding behavior without modifying the original. Implemented using closures. Used extensively in Flask/FastAPI for route registration, authentication, logging.

**Q9. What is a generator?**

A generator is a function that uses `yield` to produce values lazily, one at a time. It doesn't compute all values at once, saving memory. Essential for processing large datasets.

**Q10. What is the difference between a generator and an iterator?**

All generators are iterators. An iterator is any object with `__iter__()` and `__next__()` methods. A generator is a special way to create iterators using `yield`. Generators are simpler to write; custom iterators require implementing both methods manually.

---

## OOP Questions

**Q11. What is the difference between `__str__` and `__repr__`?**

`__str__` is for human-readable output (used by `print()`). `__repr__` is for developer/debugging output (used in the REPL and `repr()`). `__repr__` should ideally produce output that can recreate the object: `ClassName(param=value)`.

**Q12. What is the difference between instance, class, and static methods?**

```python
class MyClass:
    class_var = 0

    def instance_method(self):   # Has access to self (instance)
        pass

    @classmethod
    def class_method(cls):       # Has access to cls (the class itself)
        pass                     # Can modify class variables

    @staticmethod
    def static_method():         # No access to self or cls
        pass                     # Like a regular function inside a class
```

**Q13. What is multiple inheritance? What is the MRO?**

Multiple inheritance = a class inheriting from more than one parent.

MRO (Method Resolution Order) = the order Python searches for methods in multiple inheritance. Uses the C3 linearization algorithm.

```python
class A:
    def method(self):
        print("A")

class B(A):
    def method(self):
        print("B")

class C(A):
    def method(self):
        print("C")

class D(B, C):
    pass

D().method()   # B (MRO: D → B → C → A)
print(D.__mro__)   # (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

**Q14. What is `super()`?**

`super()` calls the parent class's method. Essential for cooperative multiple inheritance and extending parent behavior without rewriting it.

```python
class Child(Parent):
    def __init__(self):
        super().__init__()   # Run Parent's __init__
        self.extra = "child-specific"
```

**Q15. What is abstraction and how is it implemented in Python?**

Abstraction hides implementation details and exposes only necessary interfaces. Implemented using `abc.ABC` and `@abstractmethod`. Any class inheriting from an abstract class MUST implement all abstract methods or Python raises `TypeError`.

---

## Data Structure Questions

**Q16. When would you use a tuple instead of a list?**

Use a tuple when data should not change (coordinates, RGB values, database row), when you need a hashable sequence (dict key, set element), or to signal intent ("this data is fixed"). Tuples are also more memory-efficient and faster to create.

**Q17. How does a Python dictionary maintain insertion order?**

Since Python 3.7+, dictionaries maintain insertion order as part of the language specification (not just CPython implementation). Internally, Python uses a hash table with an additional array that tracks insertion order.

**Q18. What is the time complexity of `in` for list vs set?**

List: O(n) — must check each element linearly. Set: O(1) average — uses hash lookup. For large collections with frequent membership tests, always prefer sets over lists.

**Q19. How does a set handle hash collisions?**

Python sets use open addressing with probing to handle hash collisions. When two keys hash to the same bucket, Python probes neighboring slots until an empty one is found. The load factor is kept below 2/3 to minimize collisions.

**Q20. What is the difference between `dict.get()` and `dict[]`?**

`dict["key"]` raises `KeyError` if key not found. `dict.get("key")` returns `None` (or a default value) if key not found. Always use `.get()` when the key might not exist to avoid unhandled exceptions.

---

## Memory and Performance Questions

**Q21. What is reference counting in Python?**

Python tracks how many variables (references) point to each object. When the count reaches zero, the object is deallocated. You can inspect this with `sys.getrefcount()`.

**Q22. What is Python interning?**

Python pre-creates and reuses objects for small integers (-5 to 256) and some strings to save memory. This is why `a = 100; b = 100; a is b` returns `True`.

**Q23. What is garbage collection in Python?**

Python's primary garbage collection is reference counting. For circular references (object A references B, B references A, nothing else references either), Python has a cyclic garbage collector that periodically identifies and frees such cycles.

**Q24. How does `id()` work?**

`id()` returns the memory address of an object in CPython (the implementation detail). Every living object has a unique ID. After an object is deleted, its ID can be reused by a new object.

**Q25. What is the difference between `del x` and `x = None`?**

`del x` removes the variable name from the namespace. `x = None` keeps the variable but makes it point to `None`. Both decrease the reference count of the original object, potentially triggering garbage collection.

---

## More Interview Questions (26–50)

**Q26.** What is a list comprehension? When is it better than a for loop?

**Q27.** What is the `zip()` function? What does `zip(*list_of_lists)` do?

**Q28.** What is `enumerate()`? Why is it preferred over `range(len())`?

**Q29.** What is `map()`, `filter()`, `reduce()`? When would you use each?

**Q30.** What is the difference between `sorted()` and `.sort()`?

**Q31.** How do you sort a list of dictionaries by a key?
```python
users.sort(key=lambda u: u["name"])
sorted_users = sorted(users, key=lambda u: u["age"], reverse=True)
```

**Q32.** What is a defaultdict? When would you use it?
```python
from collections import defaultdict
word_count = defaultdict(int)
for word in words:
    word_count[word] += 1   # No KeyError for new keys
```

**Q33.** What is a Counter? Give a use case.
```python
from collections import Counter
freq = Counter(["apple", "mango", "apple", "banana", "mango", "apple"])
print(freq.most_common(2))   # [('apple', 3), ('mango', 2)]
```

**Q34.** What is a deque? When is it better than a list?
```python
from collections import deque
q = deque()
q.appendleft(1)    # O(1) — efficient left insert
q.popleft()        # O(1) — efficient left remove
# list.insert(0, x) and list.pop(0) are O(n) — slow for large lists
```

**Q35.** What is the walrus operator `:=`? (Python 3.8+)
```python
while chunk := file.read(1024):   # Assign and check in one step
    process(chunk)
```

**Q36.** What is the difference between `any()` and `all()`?

**Q37.** How do you flatten a nested list?
```python
nested = [[1,2],[3,4],[5,6]]
flat = [x for sublist in nested for x in sublist]
# Or: import itertools; flat = list(itertools.chain.from_iterable(nested))
```

**Q38.** What is `*` unpacking in Python 3?

**Q39.** What is the difference between `throw` and `raise` in Python?
Python uses `raise`. `throw` is from JavaScript/Java.

**Q40.** What are Python's built-in exceptions? Name 10.
```
ValueError, TypeError, KeyError, IndexError, AttributeError,
NameError, ImportError, OSError, StopIteration, RecursionError
```

**Q41.** What is a context manager? How do you create a custom one?
```python
class ManagedResource:
    def __enter__(self):
        print("Opening resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing resource")
        return False  # Don't suppress exceptions
```

**Q42.** What is the `@property` decorator?

**Q43.** What are dunder (magic) methods? Name 10.
```
__init__, __str__, __repr__, __len__, __eq__, __lt__,
__add__, __contains__, __iter__, __next__
```

**Q44.** What is method resolution order (MRO)?

**Q45.** What is `__slots__`?
```python
class Point:
    __slots__ = ['x', 'y']   # Prevents dynamic attribute creation, saves memory
```

**Q46.** What is the difference between `@classmethod` and `@staticmethod`?

**Q47.** How is Python's `dict` implemented internally?
Hash table with open addressing. Keys are hashed; bucket is found; if collision, probing.

**Q48.** What is Python's `with` statement?

**Q49.** What is the difference between `import module` and `from module import name`?

**Q50.** What is `__name__ == "__main__"` for?
Allows a file to be run directly (executes code) or imported as a module (code block skipped).

---

# SECTION 15 — 30 PRACTICE PROGRAMS

## Easy Level

**Program 1 — Check Mutability**

```python
# Problem: Demonstrate mutability difference between list and tuple
# Output: Show what changes and what doesn't

def demonstrate_mutability():
    # Mutable
    my_list = [1, 2, 3]
    id_before = id(my_list)
    my_list.append(4)
    id_after = id(my_list)
    print(f"List mutation: {id_before == id_after}")   # True — same object
    print(f"List: {my_list}")

    # Immutable
    my_tuple = (1, 2, 3)
    id_before = id(my_tuple)
    my_tuple = my_tuple + (4,)   # Creates NEW tuple
    id_after = id(my_tuple)
    print(f"Tuple reassign: {id_before == id_after}")   # False — different object
    print(f"Tuple: {my_tuple}")

demonstrate_mutability()
# List mutation: True
# List: [1, 2, 3, 4]
# Tuple reassign: False
# Tuple: (1, 2, 3, 4)
```

**Program 2 — Remove Duplicates (3 methods)**

```python
data = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

# Method 1: set (doesn't preserve order)
no_dupes_1 = list(set(data))
print(f"Set method: {sorted(no_dupes_1)}")

# Method 2: dict.fromkeys (preserves order)
no_dupes_2 = list(dict.fromkeys(data))
print(f"Dict method: {no_dupes_2}")

# Method 3: loop (educational, not recommended)
seen = set()
no_dupes_3 = []
for item in data:
    if item not in seen:
        no_dupes_3.append(item)
        seen.add(item)
print(f"Loop method: {no_dupes_3}")
```

**Program 3 — *args Calculator**

```python
def calculator(operation, *numbers):
    if not numbers:
        return 0

    results = {
        "sum":     sum(numbers),
        "product": __import__("math").prod(numbers),
        "average": sum(numbers) / len(numbers),
        "min":     min(numbers),
        "max":     max(numbers)
    }

    return results.get(operation, "Unknown operation")

print(calculator("sum", 1, 2, 3, 4, 5))       # 15
print(calculator("average", 10, 20, 30))        # 20.0
print(calculator("product", 2, 3, 4))           # 24
```

**Program 4 — Shallow vs Deep Copy Test**

```python
import copy

def test_copies():
    original = {"user": {"name": "Adya", "scores": [95, 87]}}

    # Assignment
    assignment = original
    assignment["user"]["name"] = "Changed"
    print(f"After assignment modify: original = {original['user']['name']}")
    # Changed — shared reference

    # Reset
    original = {"user": {"name": "Adya", "scores": [95, 87]}}

    # Shallow copy
    shallow = original.copy()
    shallow["user"]["name"] = "Changed"
    print(f"After shallow modify: original = {original['user']['name']}")
    # Changed — inner dict shared

    # Reset
    original = {"user": {"name": "Adya", "scores": [95, 87]}}

    # Deep copy
    deep = copy.deepcopy(original)
    deep["user"]["name"] = "Changed"
    print(f"After deep modify: original = {original['user']['name']}")
    # Adya — completely independent

test_copies()
```

**Program 5 — **kwargs Config Builder**

```python
def create_server_config(host: str, port: int, **options):
    config = {
        "host": host,
        "port": port,
        "debug": False,        # Default
        "workers": 1,          # Default
        "log_level": "info"    # Default
    }
    config.update(options)     # Override defaults with provided options
    return config

dev_config  = create_server_config("localhost", 8000, debug=True, workers=2)
prod_config = create_server_config("0.0.0.0",  8080, workers=8, log_level="error")

print("Dev:", dev_config)
print("Prod:", prod_config)
```

## Medium Level

**Program 6 — Employee Management with OOP**

```python
from datetime import date

class Employee:
    total_employees = 0
    department_registry = {}

    def __init__(self, emp_id: int, name: str, department: str, salary: float):
        self.emp_id     = emp_id
        self.name       = name
        self.department = department
        self.__salary   = salary   # Private
        self.hire_date  = date.today()
        Employee.total_employees += 1
        Employee.department_registry.setdefault(department, []).append(self)

    @property
    def salary(self) -> float:
        return self.__salary

    @salary.setter
    def salary(self, new_salary: float):
        if new_salary < 0:
            raise ValueError("Salary cannot be negative")
        if new_salary > self.__salary * 1.5:
            print(f"⚠️  Warning: Salary increase > 50% for {self.name}")
        self.__salary = new_salary

    def get_annual_salary(self) -> float:
        return self.__salary * 12

    @classmethod
    def get_department_count(cls, dept: str) -> int:
        return len(cls.department_registry.get(dept, []))

    @staticmethod
    def validate_emp_id(emp_id: int) -> bool:
        return 1000 <= emp_id <= 9999

    def __str__(self) -> str:
        return f"[{self.emp_id}] {self.name} — {self.department} — ₹{self.__salary:,.0f}/month"

    def __repr__(self) -> str:
        return f"Employee(id={self.emp_id}, name={self.name!r})"

class Manager(Employee):
    def __init__(self, emp_id: int, name: str, department: str, salary: float, team_size: int):
        super().__init__(emp_id, name, department, salary)
        self.team_size = team_size

    def get_management_bonus(self) -> float:
        return self.salary * 0.2 * (self.team_size / 10)

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} [Manager, Team: {self.team_size}]"

# Usage
emp1 = Employee(1001, "Adyaprana", "Engineering", 80000)
emp2 = Employee(1002, "Ravi", "Engineering", 75000)
emp3 = Employee(1003, "Priya", "Design", 70000)
mgr1 = Manager(2001, "Kavitha", "Engineering", 150000, 15)

print(emp1)
print(mgr1)
print(f"Engineering headcount: {Employee.get_department_count('Engineering')}")
print(f"Total employees: {Employee.total_employees}")

emp1.salary = 90000   # Use setter
print(f"Updated salary: ₹{emp1.salary:,.0f}")
print(f"Annual salary: ₹{emp1.get_annual_salary():,.0f}")
```

**Program 7 — Student Database with *args **kwargs**

```python
from typing import Optional
import copy

class StudentDatabase:
    def __init__(self):
        self.__students = {}
        self.__next_id  = 1001

    def add_student(self, name: str, *subjects, **extra_info) -> dict:
        student = {
            "id":       self.__next_id,
            "name":     name,
            "subjects": list(subjects),
            **extra_info
        }
        self.__students[self.__next_id] = student
        self.__next_id += 1
        return student

    def get_student(self, student_id: int) -> Optional[dict]:
        student = self.__students.get(student_id)
        return copy.deepcopy(student)   # Return copy — protect internal data

    def search(self, **criteria) -> list:
        results = []
        for student in self.__students.values():
            if all(student.get(k) == v for k, v in criteria.items()):
                results.append(copy.deepcopy(student))
        return results

    def all_students(self) -> list:
        return [copy.deepcopy(s) for s in self.__students.values()]

    def __len__(self) -> int:
        return len(self.__students)

db = StudentDatabase()
db.add_student("Adyaprana", "Python", "Database", "FastAPI", year=2, gpa=9.2, city="Bangalore")
db.add_student("Ravi", "Python", "React", year=2, gpa=8.5, city="Mumbai")
db.add_student("Priya", "Data Science", "ML", year=1, gpa=9.5, city="Bangalore")

print(f"Total students: {len(db)}")
print(db.get_student(1001))
bangalore_students = db.search(city="Bangalore")
print(f"Bangalore students: {len(bangalore_students)}")
```

## Hard Level

**Program 8 — Inventory System with All Concepts**

```python
import copy
from abc import ABC, abstractmethod
from typing import Optional

class Item(ABC):
    @abstractmethod
    def get_info(self) -> dict:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

class Product(Item):
    def __init__(self, sku: str, name: str, price: float, quantity: int, **attributes):
        self.__sku        = sku
        self.name         = name
        self.__price      = price
        self.__quantity   = quantity
        self.attributes   = attributes   # Extra attrs via **kwargs

    @property
    def sku(self) -> str:
        return self.__sku

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__price = value

    @property
    def quantity(self) -> int:
        return self.__quantity

    def add_stock(self, *quantities: int) -> None:
        for q in quantities:
            if q > 0:
                self.__quantity += q

    def sell(self, amount: int = 1) -> bool:
        if amount > self.__quantity:
            return False
        self.__quantity -= amount
        return True

    def is_available(self) -> bool:
        return self.__quantity > 0

    def get_info(self) -> dict:
        return {
            "sku": self.__sku,
            "name": self.name,
            "price": self.__price,
            "quantity": self.__quantity,
            "available": self.is_available(),
            **self.attributes
        }

    def __str__(self) -> str:
        return f"{self.name} (SKU: {self.__sku}) — ₹{self.__price} × {self.__quantity}"

class Inventory:
    def __init__(self):
        self.__products: dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        self.__products[product.sku] = product

    def get_product(self, sku: str) -> Optional[Product]:
        return self.__products.get(sku)

    def search(self, **filters) -> list:
        results = []
        for product in self.__products.values():
            info = product.get_info()
            if all(info.get(k) == v for k, v in filters.items()):
                results.append(product)
        return results

    def low_stock_alert(self, threshold: int = 5) -> list:
        return [p for p in self.__products.values() if 0 < p.quantity <= threshold]

    def total_value(self) -> float:
        return sum(p.price * p.quantity for p in self.__products.values())

    def snapshot(self) -> dict:
        return {sku: copy.deepcopy(p.get_info()) for sku, p in self.__products.items()}

# Usage
inv = Inventory()
inv.add_product(Product("PY001", "Python Basics Book",  599,  50, category="book",  author="Erik Westra"))
inv.add_product(Product("PY002", "FastAPI Course",       999,   3, category="course", format="video"))
inv.add_product(Product("PY003", "PostgreSQL Guide",     799,  20, category="book",  author="Simon Riggs"))

inv.get_product("PY001").add_stock(10, 20, 5)   # Add multiple quantities using *args
inv.get_product("PY002").sell(2)

print(f"Total inventory value: ₹{inv.total_value():,.0f}")
print("Low stock items:")
for p in inv.low_stock_alert(threshold=5):
    print(f"  {p}")

books = inv.search(category="book")
print(f"\nBooks: {len(books)}")
for b in books:
    print(f"  {b}")
```

---

# SECTION 16 — CHEAT SHEET

```
MUTABLE vs IMMUTABLE
  Mutable:   list, dict, set, bytearray
  Immutable: int, float, str, bool, tuple, frozenset, bytes, None

COPY TYPES
  x = y              → Same object (no copy)
  y = x.copy()       → Shallow (new container, shared inner objects)
  y = deepcopy(x)    → Deep (completely independent)

== vs is
  ==   → Compare VALUES    (use for data comparison)
  is   → Compare IDENTITY  (use only for None, True, False)

*args / **kwargs
  *args   → Extra positional → tuple inside function
  **kwargs → Extra keyword  → dict inside function
  Order: (pos, *args, keyword_only, **kwargs)

LEGB Rule
  L → Local → E → Enclosing → G → Global → B → Built-in

FALSY VALUES
  False, 0, 0.0, 0j, "", [], (), {}, set(), None

TIME COMPLEXITY
  list in  → O(n)    set/dict in → O(1)
  list get → O(1)    dict get    → O(1)
  list add → O(1)*   set add     → O(1)

GIL
  Only 1 thread executes bytecode at a time
  Released during I/O operations
  Bypass with multiprocessing for CPU-bound work

DATA STRUCTURES
  list  → ordered, mutable, duplicates   [1,2,3]
  tuple → ordered, immutable, duplicates (1,2,3)
  set   → unordered, mutable, no-dupes  {1,2,3}
  dict  → ordered(3.7+), mutable, key-value {"a":1}
```

---

# REVISION SHEET

```
TODAY'S CORE CONCEPTS

Memory Model
  → Variables are references to objects, not containers
  → id() shows memory address
  → Python interns small ints (-5 to 256) and some strings

Mutable vs Immutable
  → Mutable: list, dict, set
  → Immutable: int, str, tuple, frozenset
  → Immutable objects are hashable (can be dict keys)
  → Never use mutable default arguments!

GIL
  → One thread at a time for Python bytecode
  → Released during I/O (threads useful for I/O)
  → Use multiprocessing for CPU-bound parallelism

Data Structures at a Glance
  → list: ordered, mutable, O(n) search
  → tuple: ordered, immutable, hashable, less memory
  → set: unordered, O(1) search, no duplicates
  → dict: key-value, O(1) lookup, insertion-ordered

Copy
  → = is NOT a copy (same object)
  → .copy() is shallow (shared inner objects)
  → deepcopy() is fully independent

*args / **kwargs
  → *args → any positional args → tuple
  → **kwargs → any keyword args → dict
  → Enable flexible, reusable functions

LEGB
  → Python resolves names Local → Enclosing → Global → Built-in

Truthy/Falsy
  → Falsy: False, 0, "", [], {}, (), set(), None
  → Everything else is truthy

OOP Pillars
  → Encapsulation: hide internals, expose interface
  → Inheritance: child extends parent (super())
  → Polymorphism: same method, different behavior
  → Abstraction: ABC + @abstractmethod
```

---

## 🎥 Recommended Resource

> **Programiz Python OOP Tutorials** — clear, visual explanations
> **GeeksforGeeks Python Data Structures** — comprehensive with examples
> **Python Official Docs — Data Model** — understand __dunder__ methods

---

*Day 27 Complete.* ✅