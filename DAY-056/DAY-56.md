# DAY 56 — URL Shortener: Router Layer, HTTP Wiring + LeetCode Maximum Sum Circular Subarray

> **Phase:** 02 — FastAPI Backend (Days 43–90)
>
> **Week:** W8 — Project 1 Build (Days 50–56)
>
> **Project:** URL Shortener API v1.0 — Router Layer Complete (Architecture Finished)
>
> **LeetCode:** #918 Maximum Sum Circular Subarray ✅ (39ms · Beats 97.58%) — Kadane's Algorithm + Minimum Kadane
>
> **Status:** ✅ Day 56 Complete — url_router.py written with POST /shorten, wired into main.py with app.include_router(), architecture is now fully connected: Router → Service → Repository → Database

---

# 🎯 What Day 56 Is About

```
URL Shortener — Router Layer (HTTP Wiring)

  ✅ Why endpoints don't live directly in main.py
  ✅ APIRouter — grouping endpoints by feature
  ✅ What the Router is allowed to know (and what it must never know)
  ✅ Dependency Injection — Depends(get_db) end to end
  ✅ response_model — validating and shaping the outgoing JSON
  ✅ status_code=201 — why POST /shorten is not a 200
  ✅ Converting Pydantic HttpUrl → str before calling the Service
  ✅ Why short_url is never stored — built dynamically per environment
  ✅ app.include_router() — how main.py finds out the router exists
  ✅ The complete Client → Router → Service → Repository → Database round trip
  ✅ LeetCode #918 — Maximum Sum Circular Subarray (Kadane's + Minimum Kadane + Total Sum)
```

**Today's milestone:** The application is now a complete, working REST API. A real HTTP request — `POST /shorten` — travels through every architectural layer and comes back as a real, validated JSON response. Nothing is hardcoded, nothing is mixed together. Each layer does exactly one job.

---

# SECTION 1 — THE FUNDAMENTAL QUESTION OF DAY 56

## Where Should the Endpoint Itself Live?

```
Three options:
  Option A → Directly in main.py
  Option B → Split across many small router files, never grouped
  Option C → APIRouter, grouped by feature, included into main.py

Answer: Option C
```

---

## Why NOT Directly in `main.py`?

```python
# BAD — every endpoint dumped into main.py
from fastapi import FastAPI

app = FastAPI()

@app.post("/shorten")
def shorten_url(...): ...

@app.get("/{short_code}")
def redirect(...): ...

@app.post("/login")
def login(...): ...

@app.post("/register")
def register(...): ...

# ...50 more endpoints later
```

**Problems with this approach:**

```
main.py now does EVERYTHING:
  → URL shortening endpoints
  → Authentication endpoints
  → User management endpoints
  → App startup/shutdown config

Consequences:
  → main.py grows to thousands of lines.
  → Want to find the login endpoint? Scroll through URL logic first.
  → Two people working on different features → merge conflicts on the same file.
  → Impossible to tell, at a glance, what "areas" the API even has.

One giant file = one giant reason to step on each other's work.
```

---

## WHY the Router (`APIRouter`)?

```
APIRouter groups endpoints that belong to the SAME feature.

routers/
    url_router.py     ← everything about shortening/redirecting URLs
    auth_router.py     ← everything about login/register/tokens
    user_router.py     ← everything about user profile/settings

Each file is small, focused, and independently readable.

app.include_router(url_router)  ← main.py just plugs them in
app.include_router(auth_router)
app.include_router(user_router)

main.py becomes a thin assembly file: "here are the pieces of my API."
```

**The organizing question:** *"Which router file does this endpoint belong to?"* → answered by *what feature does it belong to*, not by *what file is smallest right now*.

---

# SECTION 2 — WHAT THE ROUTER KNOWS (AND MUST NEVER KNOW)

```
The Router knows:
  ✅ HTTP Requests        (what came in on the wire)
  ✅ HTTP Responses       (what status code, what shape)
  ✅ FastAPI Dependencies (Depends(get_db))
  ✅ Pydantic Schemas     (URLCreate, URLResponse)
  ✅ Services             (calls URLService, nothing lower)

The Router must NEVER know:
  ❌ SQL Queries          (that's the Repository)
  ❌ Database Session Internals
  ❌ Business Rules       (short code length, uniqueness — that's the Service)
```

**Why this boundary matters:** if the Router starts running SQL or generating short codes itself, the same three-layer collapse from Day 55 happens again — one file doing HTTP + business logic + database work, all at once, all fragile.

```
"Where should this line of code go?"
  → Talks to `request` or `response`? → Router.
  → Decides WHAT should happen? → Service.
  → Talks to the database directly? → Repository.
```

---

# SECTION 3 — DEPENDENCY INJECTION: `Depends(get_db)`

```python
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
    ...
```

```
Request Starts
      ↓
get_db() runs      → opens a new database Session
      ↓
Session injected   → passed into the endpoint as `db`
      ↓
Endpoint runs       → uses `db` freely
      ↓
Session closed automatically  → even if the endpoint raised an error
```

**Why not just open the session manually inside the endpoint?**

```python
# BAD — manual session management
def shorten_url(url: URLCreate):
    db = SessionLocal()
    try:
        ...
    finally:
        db.close()
```

```
Problems:
  → Every endpoint repeats the same open/close boilerplate.
  → Easy to forget db.close() → connection leak.
  → If an exception is raised before db.close(), the session may never close.

Depends(get_db) with a generator function handles this ONCE, centrally:

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

FastAPI calls get_db(), runs the endpoint with the yielded session,
then resumes get_db() after the `yield` to run db.close() — guaranteed,
even on exceptions. One function, used by every endpoint that needs a session.
```

---

# SECTION 4 — `response_model` AND `status_code=201`

## `response_model`

```python
@router.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(url: URLCreate, db: Session = Depends(get_db)):
    return url_service.create_short_url(db, str(url.original_url))
```

```
The endpoint returns a ShortenedURL SQLAlchemy model object.
response_model=URLResponse tells FastAPI:
  → Take that returned object.
  → Validate it against the URLResponse schema.
  → Convert it into exactly the JSON shape URLResponse defines.
  → Strip out any field not declared on URLResponse (e.g. internal DB columns).

Without response_model:
  → FastAPI would serialize whatever the object naturally exposes.
  → Internal fields could leak into the API response by accident.

response_model is a CONTRACT: "This is what clients will always receive,
regardless of what the internal model object actually contains."
```

## `status_code=201`

```
HTTP status codes are not decoration. They mean something specific.

200 OK       → "Here's the result of a normal request."
201 Created  → "A brand new resource now exists because of this request."

POST /shorten creates a brand new ShortenedURL row.
That is a resource creation event → 201 is the correct, REST-standard code.

If we used 200 instead:
  → Technically still "works" — client still gets JSON.
  → But it's semantically wrong, and any API consumer relying on
    standard REST conventions (e.g. auto-generated SDKs, API testing
    tools) may misinterpret the response.
```

---

# SECTION 5 — CONVERTING `HttpUrl` TO `str`

```python
url: URLCreate            # url.original_url is a Pydantic HttpUrl object
str(url.original_url)     # → plain Python string
```

```
Why does this conversion have to happen at all?

URLCreate (the incoming request schema) validates original_url as HttpUrl:
  → Pydantic automatically rejects malformed URLs before the endpoint even runs.
  → This is validation happening for free, at the schema boundary.

But URLService.create_short_url() expects a plain str:
  → The Service must not depend on Pydantic/FastAPI types (Day 55 rule:
    loose coupling — the Service shouldn't care where the string came from).

So the boundary conversion happens exactly once, in the Router:

  HttpUrl("https://google.com")
             ↓  str(...)
  "https://google.com"
             ↓
  passed into url_service.create_short_url(db, that_string)

This keeps validation (Pydantic's job) and business logic (Service's job)
cleanly separated, with the Router as the translator between them.
```

---

# SECTION 6 — WHY `short_url` IS NEVER STORED

```
short_url = Base URL + short_code

The base URL is NOT a fixed value — it changes per environment:

  Development → http://127.0.0.1:8000/Ab12Cd
  Staging     → https://staging.myurlshortener.com/Ab12Cd
  Production  → https://myurlshortener.com/Ab12Cd

If short_url were stored in the database at creation time:
  → It would be permanently wrong the moment the app moves environments.
  → A URL shortened in Development would show a localhost link forever,
    even after deploying to Production.

Instead:
  → Only short_code is stored (e.g. "Ab12Cd") — this NEVER changes.
  → short_url is built on the fly, inside the Router, at response time:

      short_url = f"{request.base_url}{db_url.short_code}"

  → Every environment automatically gets the correct, current base URL.

Storing derived data that depends on runtime context is a common mistake.
Store the minimal fact (short_code). Compute the rest when needed.
```

---

# SECTION 7 — THE COMPLETE ROUTER FILE

## `app/routers/url_router.py`

```python
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.url_schema import URLCreate, URLResponse
from app.services.url_service import URLService

router = APIRouter()
url_service = URLService()


@router.post("/shorten", response_model=URLResponse, status_code=201)
def shorten_url(
    url: URLCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Create a new shortened URL.

    Flow:
      1. FastAPI validates the incoming body against URLCreate.
      2. HttpUrl is converted to a plain string.
      3. The Service generates a unique short code and saves the record.
      4. The short_url is built dynamically from the current request's base URL.
      5. FastAPI validates and shapes the response using URLResponse.
    """
    db_url = url_service.create_short_url(db, str(url.original_url))

    return URLResponse(
        original_url=db_url.original_url,
        short_code=db_url.short_code,
        short_url=f"{request.base_url}{db_url.short_code}"
    )
```

## Wiring It Into `main.py`

```python
from fastapi import FastAPI
from app.routers.url_router import router as url_router

app = FastAPI()

app.include_router(url_router)
```

```
app.include_router(url_router)
            ↓
FastAPI registers every endpoint defined inside url_router
            ↓
POST /shorten becomes a real, reachable endpoint

Without this one line:
  → url_router.py could have perfectly correct code inside it.
  → FastAPI would never know it exists.
  → Visiting POST /shorten would return 404 Not Found.

include_router is the moment the pieces actually become one running API.
```

---

# SECTION 8 — THE COMPLETE REQUEST FLOW

```
Client sends:
  POST /shorten
  { "original_url": "https://google.com" }

            ↓

FastAPI validates the body → URLCreate (Schema)
  → Rejects the request immediately if original_url isn't a valid URL

            ↓

Router (url_router.py)
  → Depends(get_db) injects a database Session
  → Converts HttpUrl → str
  → Calls url_service.create_short_url(db, url_string)

            ↓

URLService (Day 55)
  → Generates a random 6-character short code
  → Checks uniqueness via URLRepository.get_by_short_code()
  → Retries on collision (while True loop)
  → Builds the ShortenedURL model object

            ↓

URLRepository (Day 54/55)
  → db.add(url) / db.commit() / db.refresh(url)
  → Talks to PostgreSQL directly — nothing above it does

            ↓

PostgreSQL
  → INSERT INTO shortened_urls (...)
  → UNIQUE constraint on short_code as the final safety net

            ↓

Router builds the response
  → short_url = request.base_url + short_code (never stored, always current)
  → response_model=URLResponse validates and shapes the JSON
  → status_code=201 signals "resource created"

            ↓

Client receives:
  HTTP 201 Created
  {
    "original_url": "https://google.com",
    "short_code": "Ab12Cd",
    "short_url": "http://127.0.0.1:8000/Ab12Cd"
  }
```

**This is the full architecture, end to end, for the first time:**

```
Client → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL → URLResponse (Schema) → Client
```

---

# SECTION 9 — LEETCODE #918: MAXIMUM SUM CIRCULAR SUBARRAY

## Problem

```
Given a circular integer array nums, return the maximum possible sum
of a non-empty subarray.

Circular means: the element after the last element wraps back to the first.
Each element may still be used at most once.
```

```
Example 1: nums = [1,-2,3,-2]   → 3   (best subarray: [3], wrapping doesn't help)
Example 2: nums = [5,-3,5]      → 10  (best subarray wraps: [5, _, 5])
Example 3: nums = [-3,-2,-3]    → -2  (all negative: best single element)
```

---

## First Thought

```
LeetCode #53 (Day 55) already solved "Maximum Subarray" with Kadane's Algorithm.

But Kadane's, as-is, only looks at a normal (non-wrapping) array.
This problem allows the subarray to wrap around the end back to the start.
Straight Kadane's is not enough on its own — a new observation is needed.
```

---

## The Big Observation

```
nums = [5, -3, 5]

Circular answer: 5 (wrap) 5  =  10

What got left OUT of that answer?
  -3

So instead of directly searching for the wrapping subarray,
think of it as:

  Whole Array  -  Middle Part (the part NOT included)

Which middle part should be removed to leave the LARGEST remainder?
  → The SMALLEST (minimum) contiguous subarray.

Removing the worst possible middle section leaves the best possible
circular subarray around the outside.
```

```
Circular Maximum  =  Total Sum  -  Minimum Subarray Sum

Example:
  Total Sum          = 5 + (-3) + 5 = 7
  Minimum Subarray   = -3
  Circular Answer    = 7 - (-3) = 10   ✅
```

---

## Why Two Candidates, Not One

```
There are only two possible shapes the answer can take:

Case 1 — Answer is completely inside the array (no wrapping needed)
  nums = [1, -2, 3, -2]
  Maximum Kadane = 3
  Total - Minimum = (1-2+3-2) - (-2) = 0 - (-2) = 2
  Correct answer = 3 → normal Kadane wins here.

Case 2 — Answer wraps around
  nums = [5, -3, 5]
  Maximum Kadane = 7
  Total - Minimum = 7 - (-3) = 10
  Correct answer = 10 → the circular candidate wins here.

Since either case can be correct depending on the input,
the final answer must compare BOTH candidates and take the larger one:

  answer = max(Maximum Kadane, Total Sum - Minimum Kadane)
```

---

## The Critical Edge Case: All Negative Numbers

```
nums = [-3, -2, -5]

Maximum Kadane  = -2   (best single element)
Minimum Kadane  = -10  (the entire array — all three elements)
Total Sum       = -10

Circular Formula:  Total - Minimum  =  -10 - (-10)  =  0

But 0 is IMPOSSIBLE — no subarray sums to 0 here, and the problem
requires at least one element (non-empty subarray).

Why did the formula break?
  Minimum Subarray == Total Sum
  → That means the "minimum" subarray IS the entire array.
  → Removing the entire array leaves NOTHING.
  → An empty subarray is not allowed.

Fix: if Minimum Subarray == Total Sum, the circular candidate is
invalid — just return the normal Maximum Kadane result instead.
```

---

## Complete Algorithm

```
Initialize total_sum, max_current/max_subarr, min_current/min_subarr
all to nums[0]

Traverse the array once, from index 1:
  total_sum += nums[i]

  Minimum Kadane at this index:
    min_current = min(nums[i], min_current + nums[i])
    min_subarr  = min(min_subarr, min_current)

  Maximum Kadane at this index:
    max_current = max(nums[i], max_current + nums[i])
    max_subarr  = max(max_subarr, max_current)

After the loop:
  if min_subarr == total_sum:
      return max_subarr                       # all-negative guard
  return max(max_subarr, total_sum - min_subarr)
```

---

## Final Code (Accepted — 39ms, Beats 97.58%)

```python
class Solution(object):
    def maxSubarraySumCircular(self, nums):
        total_sum = nums[0]

        min_current = nums[0]
        min_subarr = nums[0]

        max_current = nums[0]
        max_subarr = nums[0]

        for i in range(1, len(nums)):
            total_sum += nums[i]

            # Minimum Kadane
            if nums[i] < (min_current + nums[i]):
                min_current = nums[i]
            else:
                min_current += nums[i]
            if min_current < min_subarr:
                min_subarr = min_current

            # Maximum Kadane
            if nums[i] > (max_current + nums[i]):
                max_current = nums[i]
            else:
                max_current += nums[i]
            if max_current > max_subarr:
                max_subarr = max_current

        if min_subarr == total_sum:
            return max_subarr

        return max(max_subarr, total_sum - min_subarr)
```

---

## The Dry Run Table

```
Input: nums = [5, -3, 5]

Initial:  total=5   max_current=5  max_subarr=5   min_current=5  min_subarr=5

i=1, nums[1]=-3
  total = 5 + (-3) = 2
  Minimum: -3 < (5 + -3)=2 → start fresh → min_current = -3 → min_subarr = -3
  Maximum:  -3 < (5 + -3)=2 → continue    → max_current =  2 → max_subarr = 5

i=2, nums[2]=5
  total = 2 + 5 = 7
  Minimum: 5 > (-3 + 5)=2 → continue     → min_current =  2 → min_subarr = -3 (unchanged)
  Maximum: 5 < (2 + 5)=7  → continue     → max_current =  7 → max_subarr = 7

Final:  max_subarr=7   min_subarr=-3   total_sum=7

min_subarr (-3) != total_sum (7) → formula applies
answer = max(7, 7 - (-3)) = max(7, 10) = 10   ✅
```

---

## Common Mistakes

```
❌ Forgetting the all-negative edge case
   return max(max_subarr, total_sum - min_subarr)  ← fails on [-3,-2,-5]
   Always guard: if min_subarr == total_sum: return max_subarr

❌ Updating Minimum Kadane with "larger" logic instead of "smaller"
   Minimum Kadane must choose the SMALLER of (nums[i]) vs (current + nums[i])

❌ Computing only Total - Minimum and skipping normal Maximum Kadane
   Fails whenever the non-wrapping answer is actually the best one
   (e.g. [1,-2,3,-2] → circular gives 2, but the real answer is 3)

❌ Letting the minimum subarray consume the entire array
   That represents an empty circular subarray — invalid by the problem's
   "at least one element" requirement
```

---

## Pattern Recognition

```
Whenever you see:  "Circular Array" + "Maximum Sum"
Think:              Kadane's Algorithm + Minimum Kadane + Total Sum

Kadane's Family:
  #53  Maximum Subarray            → standard Kadane's                (Day 55)
  #918 Maximum Sum Circular        → Kadane's + (Total - Min Kadane)  (Day 56)
  #152 Maximum Product Subarray    → track both max AND min (signs flip)
  2D Maximum Sum Rectangle          → Kadane's applied row by row
```

---

## Complexity

```
Time:  O(n) — single pass over the array
Space: O(1) — only a handful of running variables (total, max/min current & subarr)
```

**Result:** ✅ Accepted | Runtime: 39ms (Beats 97.58%) | Memory: 15.10MB (Beats 21.98%)

---

# SECTION 10 — IMPORTANT THINGS TO KNOW

```
 1. The Router's only job is HTTP: receive a request, call the Service,
    shape the response. Nothing more.

 2. app.include_router() is what actually connects a router's endpoints
    to the running FastAPI app — writing the router file isn't enough.

 3. Depends(get_db) gives every endpoint a fresh, auto-closed database
    session, without repeating open/close boilerplate in every function.

 4. response_model is a contract: it defines exactly what shape of JSON
    a client will always receive, regardless of the internal object's shape.

 5. status_code=201 is correct for POST /shorten because a new resource
    (a ShortenedURL row) is created. 200 is for requests that don't create
    anything new.

 6. HttpUrl → str conversion happens in the Router, once, at the boundary
    between the validated request schema and the Service, which must stay
    unaware of Pydantic/FastAPI types.

 7. short_url is never stored — it's derived from short_code + the current
    request's base URL, so it's always correct regardless of environment.

 8. The full architecture is now proven end to end:
    Client → URLCreate (Schema) → Router → URLService → URLRepository
    → PostgreSQL → URLResponse (Schema) → Client

 9. LeetCode #918 extends Kadane's Algorithm (#53) with a second,
    mirrored pass: Minimum Kadane, plus a running Total Sum.

10. Circular Maximum = Total Sum - Minimum Subarray Sum — because removing
    the worst contiguous section leaves the best possible circular one.

11. The final answer is always max(Maximum Kadane, Total - Minimum Kadane) —
    never assume the circular candidate automatically wins.

12. If Minimum Subarray == Total Sum, the "minimum" IS the whole array —
    removing it would leave an empty subarray, which is invalid. Return
    Maximum Kadane directly in that case.

13. #918 is O(n) time, O(1) space — identical complexity class to #53,
    just tracking two running Kadane passes instead of one.
```

---

# REVISION SHEET

```
═══════════════════════════════════════════════════════════
DAY 56 — ROUTER LAYER + CIRCULAR KADANE'S REVISION
═══════════════════════════════════════════════════════════

ARCHITECTURE (NOW COMPLETE):
  Client → Router → Service → Repository → Database → Client
  Router:     HTTP only (request/response, Depends, schemas)
  Service:    business logic (Day 55)
  Repository: database operations (Day 54/55)

ROUTER FILE (url_router.py):
  router = APIRouter()
  url_service = URLService()

  @router.post("/shorten", response_model=URLResponse, status_code=201)
  def shorten_url(url: URLCreate, request: Request, db: Session = Depends(get_db)):
      db_url = url_service.create_short_url(db, str(url.original_url))
      return URLResponse(
          original_url=db_url.original_url,
          short_code=db_url.short_code,
          short_url=f"{request.base_url}{db_url.short_code}"
      )

WIRING (main.py):
  app.include_router(url_router)

KEY RULES:
  short_url = built dynamically, never stored
  HttpUrl → str conversion happens in the Router only
  response_model shapes the outgoing JSON; status_code=201 = "created"

CIRCULAR KADANE'S ALGORITHM (#918):
  total = max_cur = max_sub = min_cur = min_sub = nums[0]
  for i in range(1, len(nums)):
      total += nums[i]
      min_cur = min(nums[i], min_cur + nums[i]); min_sub = min(min_sub, min_cur)
      max_cur = max(nums[i], max_cur + nums[i]); max_sub = max(max_sub, max_cur)
  if min_sub == total: return max_sub          # all-negative guard
  return max(max_sub, total - min_sub)
  Time O(n), Space O(1)

KEY RULES:
  Circular Max = Total - Minimum Subarray
  Always compare against normal Maximum Kadane too
  Guard: min_sub == total → return max_sub (avoid empty-subarray case)
```

---

## LeetCode Solved This Day

| Problem | Difficulty | Topic | Status | Runtime |
|---------|-----------|-------|--------|---------|
| #918 Maximum Sum Circular Subarray | Medium | Kadane's Algorithm, Arrays | ✅ Accepted | 39ms, Beats 97.58% |

---

*Day 56 Complete. Router layer written with POST /shorten, wired into main.py via app.include_router(). The URL Shortener API now has a fully connected architecture — Router → Service → Repository → Database — proven end to end with a real request/response cycle.* ✅