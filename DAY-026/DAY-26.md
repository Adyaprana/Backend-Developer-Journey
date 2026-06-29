# DAY 26 — PYTHON REQUESTS LIBRARY: CALLING APIs FROM PYTHON

> **Goal:** Learn how to call real APIs from Python using the `requests` library — fetch data, send data, handle responses, and build two real projects.
>
> **Week:** W4 — How the Web Works + Git + Advanced Python
>
> **Status:** ✅

---

# 🎯 Learning Roadmap

```
Python Requests Library — Calling APIs from Python

  ✅ pip install requests
  ✅ requests.get(), requests.post() with JSON body
  ✅ Handle response: .json(), .status_code, .headers
  ✅ Build: Python script that fetches GitHub profile data
  ✅ Build: Weather fetcher using OpenWeatherMap free API

  ▶ Corey Schafer: Requests Library (English)
```

## Core Concepts Checklist

- [ ] What the `requests` library is and why it exists
- [ ] How to install and import requests
- [ ] How to make a GET request and read the response
- [ ] What the Response object contains
- [ ] `.status_code`, `.text`, `.json()`, `.headers`
- [ ] How to make a POST request with a JSON body
- [ ] How to send headers with a request (API keys, tokens)
- [ ] How to send query parameters
- [ ] Timeout — why it's critical, never skip it
- [ ] Error handling — professional try/except pattern
- [ ] All 5 HTTP methods: GET, POST, PUT, PATCH, DELETE
- [ ] GitHub Profile Fetcher project
- [ ] Weather Fetcher project

---

# WHY THIS DAY IS IMPORTANT

As a backend developer, your server will constantly talk to other services:

```
Your FastAPI app → GitHub API      (to verify a user's GitHub profile)
Your FastAPI app → Razorpay API    (to process payments)
Your FastAPI app → SendGrid API    (to send emails)
Your FastAPI app → OpenAI API      (to use AI features)
Your FastAPI app → Google Maps API (to validate addresses)
Your FastAPI app → Your own DB API (microservices talking to each other)
```

All of this communication happens over HTTP.

The `requests` library is the tool Python uses to make HTTP calls.

It is the **most downloaded Python package of all time** (over 300 million downloads per month).

After today you will be able to call any API in the world from Python.

---

# SECTION 1 — WHAT IS THE requests LIBRARY?

## THE PROBLEM IT SOLVES

Python has a built-in library called `urllib` for making HTTP requests. Here is what making a simple GET request looks like with it:

```python
# urllib — the built-in but painful way
import urllib.request
import json

url = "https://api.github.com/users/octocat"
req = urllib.request.Request(url)

with urllib.request.urlopen(req) as response:
    raw = response.read()
    encoding = response.info().get_content_charset("utf-8")
    data = json.loads(raw.decode(encoding))
    print(data["login"])
```

Now here is the same thing with `requests`:

```python
# requests — clean, readable, human-friendly
import requests

response = requests.get("https://api.github.com/users/octocat")
data = response.json()
print(data["login"])
```

**Same result. Dramatically less code. Much more readable.**

This is why Kenneth Reitz created `requests` in 2011 with the tagline: **"HTTP for Humans"**

---

## INSTALLATION

```bash
# Install with pip
pip install requests

# Verify installation
python -c "import requests; print(requests.__version__)"
# Output: 2.31.0 (or similar)
```

In a project with `requirements.txt`:

```text
requests==2.31.0
```

Install from requirements file:

```bash
pip install -r requirements.txt
```

---

## IMPORT

```python
import requests
```

That's it. One import. You now have access to everything.

---

# SECTION 2 — YOUR FIRST GET REQUEST

## WHAT IS A GET REQUEST?

**GET** = "Give me data from the server."

When you type `https://github.com` in your browser, your browser sends a GET request.

You are saying: "Give me the GitHub homepage."

With `requests`, you can do the same thing from Python.

---

## THE SIMPLEST GET REQUEST

```python
import requests

response = requests.get("https://api.github.com/users/octocat")

print(response)
# <Response [200]>
```

That's it. You just made an HTTP request from Python.

`<Response [200]>` means: the server responded with status code 200 (Success).

---

## THE RESPONSE OBJECT

`requests.get()` returns a **Response object**.

Think of it as a package delivered to you. The package contains:

```
Response Object
├── .status_code    → Was it successful? (200, 404, 500, etc.)
├── .text           → Response body as raw text (string)
├── .json()         → Response body parsed as Python dict/list
├── .headers        → Metadata about the response
├── .url            → The final URL that was called
├── .content        → Response body as raw bytes (for images/files)
└── .elapsed        → How long the request took
```

---

## .status_code

The status code tells you if your request succeeded.

```python
import requests

response = requests.get("https://api.github.com/users/octocat")

print(response.status_code)   # 200

# Check if successful
if response.status_code == 200:
    print("Success!")
else:
    print(f"Something went wrong: {response.status_code}")
```

**Status codes you must know:**

```
2xx — Success
  200  OK               → Request worked perfectly
  201  Created          → Something was created (POST success)
  204  No Content       → Success but no data returned (DELETE success)

4xx — Your fault (client error)
  400  Bad Request      → You sent invalid data
  401  Unauthorized     → You need to log in / provide API key
  403  Forbidden        → Logged in but not allowed
  404  Not Found        → That URL/resource doesn't exist
  422  Unprocessable    → Data format is wrong (FastAPI validation)
  429  Too Many Requests → You're calling the API too fast (rate limited)

5xx — Server's fault
  500  Internal Error   → The server crashed
  502  Bad Gateway      → Proxy or gateway issue
  503  Unavailable      → Server is down for maintenance
```

**Shortcut to check success:**

```python
import requests

response = requests.get("https://api.github.com/users/octocat")

# .ok returns True if status code is 200-399
if response.ok:
    print("Request was successful")

# raise_for_status() raises an exception if 4xx or 5xx
response.raise_for_status()   # Raises HTTPError if failed
```

---

## .text

Returns the raw response body as a **string**.

```python
import requests

response = requests.get("https://api.github.com/users/octocat")
print(response.text)

# Output (truncated):
# {"login":"octocat","id":583231,"node_id":"MDQ6VXNlcjU4MzIzMQ==",
#  "avatar_url":"https://avatars.githubusercontent.com/u/583231?v=4",
#  "name":"The Octocat","company":"@github","blog":"https://github.blog",
#  "followers":9000,...}
```

This is a JSON string. It looks like a Python dictionary but it is actually just text.

To work with it as Python data, you need `.json()`.

---

## .json()

Converts the JSON text response into a **Python dictionary or list**.

```python
import requests

response = requests.get("https://api.github.com/users/octocat")
data = response.json()

print(type(data))           # <class 'dict'>
print(data["login"])        # octocat
print(data["name"])         # The Octocat
print(data["followers"])    # 9000+
print(data["public_repos"]) # 8+
print(data["html_url"])     # https://github.com/octocat
```

**The mental model:**

```
API returns:      '{"login": "octocat", "followers": 9000}'
                  ↑ This is a STRING (JSON text)

.json() converts: {"login": "octocat", "followers": 9000}
                  ↑ This is a Python DICTIONARY

You can now:      data["login"]     → "octocat"
                  data["followers"] → 9000
```

**What if the response is a list?**

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts")
data = response.json()

print(type(data))         # <class 'list'>
print(len(data))          # 100
print(data[0])            # {'userId': 1, 'id': 1, 'title': '...', 'body': '...'}
print(data[0]["title"])   # first post title
```

---

## .headers

Response headers are **metadata** about the response.

They tell you things like: what type of data was returned, how to cache it, rate limits remaining, etc.

```python
import requests

response = requests.get("https://api.github.com/users/octocat")

# Print all headers
print(dict(response.headers))

# Access specific header
print(response.headers["Content-Type"])
# application/json; charset=utf-8

print(response.headers.get("X-RateLimit-Remaining"))
# 59  (GitHub allows 60 requests/hour without auth)

print(response.headers.get("X-RateLimit-Limit"))
# 60
```

**Common response headers:**

```
Content-Type         → What format the data is in (application/json, text/html)
Content-Length       → Size of response in bytes
Cache-Control        → How long to cache this response
X-RateLimit-Limit    → Max requests allowed per time period
X-RateLimit-Remaining → How many requests you have left
Date                 → When the response was sent
```

---

## .url

Shows the final URL that was called (useful when redirects happen or you built a URL with params):

```python
import requests

response = requests.get(
    "https://api.github.com/users/octocat",
    params={"per_page": 10}
)

print(response.url)
# https://api.github.com/users/octocat?per_page=10
```

---

## .elapsed

How long the request took:

```python
import requests

response = requests.get("https://api.github.com/users/octocat")
print(response.elapsed.total_seconds())
# 0.234  (234 milliseconds)
```

---

# SECTION 3 — SENDING REQUEST HEADERS

## WHY YOU SEND HEADERS

Headers are extra information you attach to your request.

Most common reasons:

```
Authorization: Bearer <token>    → Prove who you are (API key, JWT)
Content-Type: application/json   → Tell server what format you're sending
Accept: application/json         → Tell server what format you want back
User-Agent: MyApp/1.0            → Tell server what app is making the request
```

## HOW TO SEND HEADERS

```python
import requests

headers = {
    "Authorization": "Bearer YOUR_TOKEN_HERE",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "MyPythonApp/1.0"
}

response = requests.get(
    "https://api.github.com/user",
    headers=headers
)
```

## GITHUB API WITH AUTHENTICATION

Without authentication, GitHub allows only 60 requests/hour.

With a Personal Access Token: 5,000 requests/hour.

```python
import requests

GITHUB_TOKEN = "ghp_YourTokenHere"

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

response = requests.get(
    "https://api.github.com/user",
    headers=headers,
    timeout=5
)

data = response.json()
print(f"Logged in as: {data['login']}")
print(f"Rate limit remaining: {response.headers['X-RateLimit-Remaining']}")
```

---

# SECTION 4 — QUERY PARAMETERS

## WHAT ARE QUERY PARAMETERS?

Query parameters filter, sort, or paginate data in a GET request.

They go after the `?` in a URL:

```
https://api.github.com/search/repositories?q=fastapi&sort=stars&per_page=5
```

Here: `q=fastapi`, `sort=stars`, `per_page=5` are query parameters.

## HOW TO SEND QUERY PARAMETERS

```python
import requests

# BAD way — building URL manually (error-prone)
url = "https://api.github.com/search/repositories?q=fastapi&sort=stars&per_page=5"
response = requests.get(url)

# GOOD way — use params dict (requests builds URL for you)
params = {
    "q": "fastapi",
    "sort": "stars",
    "per_page": 5
}
response = requests.get(
    "https://api.github.com/search/repositories",
    params=params
)

print(response.url)
# https://api.github.com/search/repositories?q=fastapi&sort=stars&per_page=5
```

The `params` dictionary approach is better because:

```
✅ Handles URL encoding automatically (spaces become %20, etc.)
✅ No mistakes building the URL manually
✅ Easier to read and change values
```

---

# SECTION 5 — TIMEOUT (NEVER SKIP THIS)

## WHY TIMEOUT IS CRITICAL

Without a timeout:

```python
response = requests.get("https://some-slow-api.com/data")
# If the server never responds, this line hangs FOREVER
# Your program is stuck
# Your backend server is stuck
# Your users are waiting forever
```

This is a real production issue. Servers crash, networks fail, external APIs go down. Without timeout, your program hangs indefinitely.

## ALWAYS USE TIMEOUT

```python
import requests

# Always pass timeout (in seconds)
response = requests.get(
    "https://api.github.com/users/octocat",
    timeout=5   # Wait maximum 5 seconds, then raise an exception
)
```

## CONNECT TIMEOUT vs READ TIMEOUT

```python
# Single number: applies to both connecting and reading
timeout=5

# Tuple: (connect_timeout, read_timeout)
timeout=(3, 10)
# Connect to server within 3 seconds
# Read the response within 10 seconds
```

---

# SECTION 6 — ERROR HANDLING (PROFESSIONAL PATTERN)

## THE TYPES OF ERRORS

```
requests.exceptions.ConnectionError    → No internet, server down, DNS failed
requests.exceptions.Timeout            → Request took too long
requests.exceptions.HTTPError          → 4xx or 5xx status code (from raise_for_status())
requests.exceptions.TooManyRedirects   → Server keeps redirecting
requests.exceptions.RequestException   → Base class for all requests errors
```

## BASIC ERROR HANDLING

```python
import requests

try:
    response = requests.get(
        "https://api.github.com/users/octocat",
        timeout=5
    )
    response.raise_for_status()   # Raise exception for 4xx and 5xx
    data = response.json()
    print(data["login"])

except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to server. Check your internet connection.")

except requests.exceptions.Timeout:
    print("❌ Request timed out. Server took too long to respond.")

except requests.exceptions.HTTPError as e:
    print(f"❌ HTTP Error: {e.response.status_code}")
    if e.response.status_code == 404:
        print("User not found.")
    elif e.response.status_code == 401:
        print("Unauthorized. Check your API key.")
    elif e.response.status_code == 429:
        print("Rate limited. Slow down your requests.")

except requests.exceptions.RequestException as e:
    # Catch-all for any other requests error
    print(f"❌ Request failed: {e}")
```

## PROFESSIONAL REUSABLE WRAPPER

```python
import requests
from typing import Optional

def safe_get(url: str, headers: dict = None, params: dict = None, timeout: int = 5) -> Optional[dict]:
    """
    A safe wrapper around requests.get() that handles all errors.
    Returns the JSON data dict, or None if anything went wrong.
    """
    try:
        response = requests.get(
            url,
            headers=headers or {},
            params=params or {},
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print(f"❌ Connection failed: {url}")
    except requests.exceptions.Timeout:
        print(f"❌ Timeout after {timeout}s: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP {e.response.status_code}: {url}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")

    return None


# Usage
data = safe_get("https://api.github.com/users/octocat")
if data:
    print(data["login"])
```

---

# SECTION 7 — POST REQUESTS (SENDING DATA)

## WHAT IS A POST REQUEST?

**POST** = "I want to send data to the server to create something."

Examples:

```
POST /users         → Create a new user account
POST /orders        → Place a new order
POST /login         → Log in with credentials
POST /messages      → Send a message
```

## HOW TO MAKE A POST REQUEST

```python
import requests

# The data you want to send
payload = {
    "name": "Adyaprana",
    "course": "MCA",
    "year": 2
}

response = requests.post(
    "https://httpbin.org/post",   # httpbin.org echoes back what you send
    json=payload                   # json= automatically sets Content-Type: application/json
)

print(response.status_code)   # 200
print(response.json())
```

## json= vs data= — What's the Difference?

```python
# json= → Automatically serializes dict to JSON string
#          Automatically sets Content-Type: application/json
#          Use this for REST APIs
response = requests.post(url, json={"name": "Adya"})

# data= → Sends form-encoded data (like HTML forms)
#          Sets Content-Type: application/x-www-form-urlencoded
#          Use this for HTML form submissions
response = requests.post(url, data={"name": "Adya"})

# data= with a string → Sends raw string body
response = requests.post(url, data='{"name": "Adya"}', headers={"Content-Type": "application/json"})
```

**For REST APIs: always use `json=`**

---

# SECTION 8 — ALL HTTP METHODS WITH requests

```python
import requests

url = "https://reqres.in/api/users"

# GET — Retrieve data
response = requests.get(f"{url}/2")
print("GET:", response.status_code, response.json())

# POST — Create new resource
response = requests.post(url, json={"name": "Adyaprana", "job": "developer"})
print("POST:", response.status_code, response.json())

# PUT — Replace entire resource
response = requests.put(f"{url}/2", json={"name": "Adyaprana", "job": "senior developer"})
print("PUT:", response.status_code, response.json())

# PATCH — Update part of resource
response = requests.patch(f"{url}/2", json={"job": "lead developer"})
print("PATCH:", response.status_code, response.json())

# DELETE — Remove resource
response = requests.delete(f"{url}/2")
print("DELETE:", response.status_code)   # 204 No Content
```

**Summary:**

```
requests.get(url)                      → Read
requests.post(url, json=data)          → Create
requests.put(url, json=data)           → Replace
requests.patch(url, json=data)         → Update
requests.delete(url)                   → Delete
```

---

# SECTION 9 — USING SESSION OBJECTS

## WHAT IS A SESSION?

A `Session` object lets you make multiple requests to the same server efficiently.

Benefits:

```
✅ Reuses the same TCP connection (faster)
✅ Persists headers across requests (set once, used everywhere)
✅ Stores cookies automatically between requests
✅ Better performance for multiple requests to same server
```

```python
import requests

# Without Session (new connection every request — slower)
r1 = requests.get("https://api.github.com/users/octocat", headers={"Authorization": "token abc"})
r2 = requests.get("https://api.github.com/users/torvalds", headers={"Authorization": "token abc"})
r3 = requests.get("https://api.github.com/users/gvanrossum", headers={"Authorization": "token abc"})

# With Session (one connection, headers set once — faster + cleaner)
with requests.Session() as session:
    session.headers.update({
        "Authorization": "token abc",
        "Accept": "application/vnd.github.v3+json"
    })

    r1 = session.get("https://api.github.com/users/octocat")
    r2 = session.get("https://api.github.com/users/torvalds")
    r3 = session.get("https://api.github.com/users/gvanrossum")
```

Use `Session` when you make multiple requests to the same API.

---

# SECTION 10 — PROJECT 1: GITHUB PROFILE FETCHER

## UNDERSTANDING THE GITHUB API

GitHub has a free public API that doesn't require authentication for basic data.

Base URL: `https://api.github.com`

Endpoint for user profile: `GET /users/{username}`

Returns JSON with user data.

---

## SIMPLE VERSION

```python
import requests

def get_github_profile(username: str) -> dict:
    """Fetch a GitHub user's public profile."""
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, timeout=5)

    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        return None
    else:
        return None

def display_profile(data: dict) -> None:
    """Display profile data in a readable format."""
    print("\n" + "=" * 40)
    print("      GITHUB PROFILE")
    print("=" * 40)
    print(f"Username:    {data.get('login', 'N/A')}")
    print(f"Name:        {data.get('name', 'N/A')}")
    print(f"Bio:         {data.get('bio', 'N/A')}")
    print(f"Company:     {data.get('company', 'N/A')}")
    print(f"Location:    {data.get('location', 'N/A')}")
    print(f"Followers:   {data.get('followers', 0)}")
    print(f"Following:   {data.get('following', 0)}")
    print(f"Public Repos:{data.get('public_repos', 0)}")
    print(f"Profile URL: {data.get('html_url', 'N/A')}")
    print(f"Blog:        {data.get('blog', 'N/A')}")
    print("=" * 40)

# Main program
username = input("Enter GitHub username: ").strip()
profile = get_github_profile(username)

if profile:
    display_profile(profile)
else:
    print(f"❌ User '{username}' not found on GitHub.")
```

---

## COMPLETE VERSION WITH ERROR HANDLING AND REPOS

```python
import requests
from datetime import datetime

def get_github_profile(username: str) -> dict | None:
    """
    Fetch GitHub profile with full error handling.
    Returns None if user not found or request fails.
    """
    url = f"https://api.github.com/users/{username}"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "GitHubProfileFetcher/1.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"❌ User '{username}' not found.")
        elif e.response.status_code == 403:
            print("❌ Rate limit exceeded. Wait a moment and try again.")
        else:
            print(f"❌ HTTP Error {e.response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ No internet connection.")
    except requests.exceptions.Timeout:
        print("❌ GitHub API is taking too long. Try again.")

    return None

def get_user_repos(username: str, limit: int = 5) -> list:
    """
    Fetch user's top repositories sorted by stars.
    """
    url = f"https://api.github.com/users/{username}/repos"
    params = {
        "sort": "stars",
        "direction": "desc",
        "per_page": limit
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return []

def format_date(iso_date: str) -> str:
    """Convert ISO date string to readable format."""
    if not iso_date:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+00:00"))
        return dt.strftime("%B %d, %Y")
    except:
        return iso_date

def display_full_profile(profile: dict, repos: list) -> None:
    """Display a beautifully formatted GitHub profile."""
    print("\n" + "=" * 50)
    print("           🐙 GITHUB PROFILE")
    print("=" * 50)
    print(f"  Username:     @{profile.get('login', 'N/A')}")
    print(f"  Name:         {profile.get('name') or 'Not set'}")
    print(f"  Bio:          {profile.get('bio') or 'No bio'}")
    print(f"  Location:     {profile.get('location') or 'Not set'}")
    print(f"  Company:      {profile.get('company') or 'Not set'}")
    print(f"  Blog/Website: {profile.get('blog') or 'Not set'}")
    print(f"  Email:        {profile.get('email') or 'Not public'}")
    print(f"  Twitter:      {('@' + profile['twitter_username']) if profile.get('twitter_username') else 'Not set'}")
    print()
    print("  📊 STATISTICS")
    print(f"  Public Repos:  {profile.get('public_repos', 0):,}")
    print(f"  Followers:     {profile.get('followers', 0):,}")
    print(f"  Following:     {profile.get('following', 0):,}")
    print(f"  Public Gists:  {profile.get('public_gists', 0):,}")
    print()
    print("  📅 ACCOUNT INFO")
    print(f"  Account Type:  {profile.get('type', 'N/A')}")
    print(f"  Joined GitHub: {format_date(profile.get('created_at'))}")
    print(f"  Last Updated:  {format_date(profile.get('updated_at'))}")
    print(f"  Profile URL:   {profile.get('html_url', 'N/A')}")

    if repos:
        print()
        print(f"  ⭐ TOP {len(repos)} REPOSITORIES")
        print("  " + "-" * 46)
        for i, repo in enumerate(repos, 1):
            stars    = repo.get("stargazers_count", 0)
            forks    = repo.get("forks_count", 0)
            language = repo.get("language") or "Unknown"
            desc     = repo.get("description") or "No description"
            if len(desc) > 40:
                desc = desc[:40] + "..."
            print(f"  {i}. {repo['name']}")
            print(f"     ⭐ {stars:,} stars  🍴 {forks:,} forks  [{language}]")
            print(f"     {desc}")

    print("=" * 50)

def main():
    print("🐙 GitHub Profile Fetcher")
    print("─" * 30)

    username = input("Enter GitHub username: ").strip()
    if not username:
        print("❌ Username cannot be empty.")
        return

    print(f"\n🔍 Searching for '{username}'...")

    profile = get_github_profile(username)
    if not profile:
        return

    repos = get_user_repos(username, limit=5)
    display_full_profile(profile, repos)

if __name__ == "__main__":
    main()
```

**Sample output for `Adyaprana`:**

```
🐙 GitHub Profile Fetcher
──────────────────────────────
Enter GitHub username: Adyaprana

🔍 Searching for 'Adyaprana'...

==================================================
           🐙 GITHUB PROFILE
==================================================
  Username:     @Adyaprana
  Name:         Adyaprana Pradhan
  Bio:          Backend Developer Journey
  Location:     Bangalore, India
  ...
  📊 STATISTICS
  Public Repos:  12
  Followers:     45
  Following:     30
  ...
==================================================
```

---

# SECTION 11 — PROJECT 2: WEATHER FETCHER

## UNDERSTANDING THE OPENWEATHERMAP API

OpenWeatherMap offers a free API tier:

```
Free tier: 60 calls/minute, 1,000,000 calls/month
API Docs: https://openweathermap.org/current
```

Getting your free API key:

```
1. Go to https://openweathermap.org/
2. Click "Sign Up" (free)
3. After registration, go to "My API Keys"
4. Copy your API key
5. Wait 10-15 minutes for the key to activate
```

**API Endpoint:**

```
https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric
```

Parameters:

```
q     → City name (e.g., "Bangalore" or "Bangalore,IN")
appid → Your API key
units → "metric" (Celsius), "imperial" (Fahrenheit), "standard" (Kelvin)
```

---

## SIMPLE VERSION

```python
import requests

API_KEY = "your_api_key_here"   # Get free at openweathermap.org

city = input("Enter city name: ").strip()

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"   # Celsius
}

response = requests.get(url, params=params, timeout=5)

if response.status_code == 200:
    data = response.json()
    print("\n===== WEATHER =====")
    print(f"City:        {data['name']}, {data['sys']['country']}")
    print(f"Temperature: {data['main']['temp']}°C")
    print(f"Feels Like:  {data['main']['feels_like']}°C")
    print(f"Humidity:    {data['main']['humidity']}%")
    print(f"Condition:   {data['weather'][0]['description'].title()}")
elif response.status_code == 404:
    print(f"City '{city}' not found.")
elif response.status_code == 401:
    print("Invalid API key. Check your OpenWeatherMap account.")
else:
    print(f"Error: {response.status_code}")
```

---

## UNDERSTANDING THE WEATHER API RESPONSE

The API returns a nested JSON. Let's understand every field:

```json
{
  "coord": {"lon": 77.5946, "lat": 12.9716},
  "weather": [
    {
      "id": 801,
      "main": "Clouds",
      "description": "few clouds",
      "icon": "02d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 28.5,
    "feels_like": 31.2,
    "temp_min": 26.0,
    "temp_max": 30.1,
    "pressure": 1013,
    "humidity": 65
  },
  "visibility": 10000,
  "wind": {
    "speed": 3.6,
    "deg": 240
  },
  "clouds": {"all": 20},
  "dt": 1719567890,
  "sys": {
    "type": 2,
    "id": 2093467,
    "country": "IN",
    "sunrise": 1719538200,
    "sunset": 1719584760
  },
  "timezone": 19800,
  "id": 1277333,
  "name": "Bangalore",
  "cod": 200
}
```

Accessing the data:

```python
data["name"]                          # "Bangalore"
data["sys"]["country"]                # "IN"
data["main"]["temp"]                  # 28.5
data["main"]["feels_like"]            # 31.2
data["main"]["humidity"]              # 65
data["main"]["pressure"]              # 1013
data["weather"][0]["description"]     # "few clouds"
data["weather"][0]["main"]            # "Clouds"
data["wind"]["speed"]                 # 3.6
data["visibility"]                    # 10000
data["clouds"]["all"]                 # 20 (% cloud cover)
```

---

## COMPLETE VERSION WITH FULL FEATURES

```python
import requests
from datetime import datetime, timezone, timedelta

API_KEY = "your_api_key_here"   # Replace with your OpenWeatherMap API key

def kelvin_to_celsius(kelvin: float) -> float:
    return round(kelvin - 273.15, 1)

def unix_to_time(unix_timestamp: int, timezone_offset: int) -> str:
    """Convert Unix timestamp to local time string."""
    utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%I:%M %p")

def get_wind_direction(degrees: int) -> str:
    """Convert wind degrees to compass direction."""
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(degrees / 45) % 8
    return directions[index]

def get_uv_advice(uv_index: float) -> str:
    if uv_index < 3:
        return "Low — no protection needed"
    elif uv_index < 6:
        return "Moderate — wear sunscreen"
    elif uv_index < 8:
        return "High — sunscreen + hat"
    elif uv_index < 11:
        return "Very High — avoid midday sun"
    else:
        return "Extreme — stay indoors"

def get_weather_emoji(condition: str) -> str:
    """Return an emoji for the weather condition."""
    condition = condition.lower()
    if "thunderstorm" in condition:
        return "⛈️"
    elif "drizzle" in condition or "rain" in condition:
        return "🌧️"
    elif "snow" in condition:
        return "❄️"
    elif "mist" in condition or "fog" in condition or "haze" in condition:
        return "🌫️"
    elif "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "⛅"
    else:
        return "🌡️"

def fetch_current_weather(city: str) -> dict | None:
    """Fetch current weather data for a city."""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 404:
            print(f"❌ City '{city}' not found. Try adding country code (e.g., 'Delhi,IN')")
            return None
        elif response.status_code == 401:
            print("❌ Invalid API key. Get a free key at openweathermap.org")
            return None

        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        print("❌ No internet connection.")
    except requests.exceptions.Timeout:
        print("❌ Weather API is slow. Try again.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")

    return None

def display_weather(data: dict) -> None:
    """Display weather data in a beautiful format."""
    city      = data["name"]
    country   = data["sys"]["country"]
    condition = data["weather"][0]["description"].title()
    emoji     = get_weather_emoji(data["weather"][0]["description"])
    tz_offset = data.get("timezone", 0)

    temp       = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    temp_min   = data["main"]["temp_min"]
    temp_max   = data["main"]["temp_max"]
    humidity   = data["main"]["humidity"]
    pressure   = data["main"]["pressure"]

    wind_speed = data["wind"]["speed"]
    wind_dir   = get_wind_direction(data["wind"].get("deg", 0))

    visibility = data.get("visibility", 0) / 1000   # Convert m to km
    clouds     = data["clouds"]["all"]

    sunrise = unix_to_time(data["sys"]["sunrise"], tz_offset)
    sunset  = unix_to_time(data["sys"]["sunset"],  tz_offset)

    print("\n" + "=" * 50)
    print(f"  {emoji}  WEATHER — {city}, {country}")
    print("=" * 50)
    print(f"  Condition:    {condition}")
    print(f"  Temperature:  {temp}°C  (Feels like {feels_like}°C)")
    print(f"  Range:        {temp_min}°C — {temp_max}°C")
    print()
    print(f"  💧 Humidity:  {humidity}%")
    print(f"  🌬️  Wind:      {wind_speed} m/s  {wind_dir}")
    print(f"  👁️  Visibility: {visibility:.1f} km")
    print(f"  ☁️  Cloud Cover: {clouds}%")
    print(f"  🔴 Pressure:  {pressure} hPa")
    print()
    print(f"  🌅 Sunrise:   {sunrise}")
    print(f"  🌇 Sunset:    {sunset}")
    print("=" * 50)

    # Weather advice
    print("\n  💡 ADVICE:")
    if humidity > 80:
        print("  • Very humid. Light clothes recommended.")
    if wind_speed > 10:
        print("  • Strong winds. Be careful outdoors.")
    if temp > 35:
        print("  • Very hot. Stay hydrated, avoid midday sun.")
    elif temp < 10:
        print("  • Cold. Wear warm layers.")
    if "rain" in condition.lower():
        print("  • Carry an umbrella!")
    if "clear" in condition.lower():
        print("  • Great weather to be outside!")

def get_weather_for_multiple_cities(cities: list) -> None:
    """Fetch and compare weather for multiple cities."""
    print(f"\n📍 Comparing weather for {len(cities)} cities:\n")
    print(f"  {'City':<20} {'Temp':>6} {'Humidity':>9} {'Condition':<20}")
    print("  " + "-" * 58)

    for city in cities:
        data = fetch_current_weather(city)
        if data:
            temp      = data["main"]["temp"]
            humidity  = data["main"]["humidity"]
            condition = data["weather"][0]["description"].title()
            name      = f"{data['name']}, {data['sys']['country']}"
            print(f"  {name:<20} {temp:>5.1f}°C {humidity:>8}%  {condition:<20}")

def main():
    print("🌤️  Python Weather Fetcher")
    print("─" * 30)
    print("Powered by OpenWeatherMap API\n")

    while True:
        print("Options:")
        print("  1. Check one city")
        print("  2. Compare multiple cities")
        print("  3. Exit")

        choice = input("\nChoice (1/2/3): ").strip()

        if choice == "1":
            city = input("Enter city name: ").strip()
            if city:
                print(f"\n🔍 Fetching weather for '{city}'...")
                data = fetch_current_weather(city)
                if data:
                    display_weather(data)

        elif choice == "2":
            cities_input = input("Enter cities separated by comma (e.g., Mumbai,Delhi,Bangalore): ")
            cities = [c.strip() for c in cities_input.split(",") if c.strip()]
            if cities:
                get_weather_for_multiple_cities(cities)

        elif choice == "3":
            print("Goodbye! 🌤️")
            break

        else:
            print("Invalid choice. Enter 1, 2, or 3.")

        print()

if __name__ == "__main__":
    main()
```

---

## TESTING WITHOUT AN API KEY

You can test the structure with JSONPlaceholder or ReqRes:

```python
import requests

# Use JSONPlaceholder (no API key needed)
response = requests.get("https://jsonplaceholder.typicode.com/users/1")
data = response.json()
print(data["name"])       # Leanne Graham
print(data["email"])      # Sincere@april.biz
print(data["phone"])      # 1-770-736-8031 x56442

# Use ReqRes (no API key needed)
response = requests.post(
    "https://reqres.in/api/login",
    json={"email": "eve.holt@reqres.in", "password": "cityslicka"}
)
print(response.status_code)  # 200
print(response.json())       # {'token': 'QpwL5tpe83ilfN2'}
```

---

# SECTION 12 — WORKING WITH REAL APIs (QUICK REFERENCES)

## REQRES API (Practice — No Key Needed)

```python
import requests

BASE = "https://reqres.in/api"

# List users
r = requests.get(f"{BASE}/users?page=1")
users = r.json()["data"]
for u in users:
    print(f"{u['first_name']} {u['last_name']} — {u['email']}")

# Create user
r = requests.post(f"{BASE}/users", json={"name": "Adyaprana", "job": "developer"})
print(r.status_code, r.json())   # 201

# Login
r = requests.post(f"{BASE}/login", json={"email": "eve.holt@reqres.in", "password": "cityslicka"})
print(r.json())   # {'token': 'QpwL5tpe83ilfN2'}

# Failed login
r = requests.post(f"{BASE}/login", json={"email": "peter@klaven.com"})
print(r.status_code, r.json())   # 400, {'error': 'Missing password'}
```

---

## HTTPBIN API (Inspect What You Send)

```python
import requests

# See exactly what headers you're sending
r = requests.get("https://httpbin.org/headers")
print(r.json())

# See your IP address
r = requests.get("https://httpbin.org/ip")
print(r.json())   # {'origin': '49.xx.xx.xx'}

# Test POST body
r = requests.post("https://httpbin.org/post", json={"test": "data"})
print(r.json()["json"])   # {'test': 'data'}  (what the server received)

# Test timeout (server delays response by 3 seconds)
try:
    r = requests.get("https://httpbin.org/delay/3", timeout=2)
except requests.exceptions.Timeout:
    print("Timed out as expected!")

# Test specific status codes
r = requests.get("https://httpbin.org/status/404")
print(r.status_code)   # 404

r = requests.get("https://httpbin.org/status/500")
print(r.status_code)   # 500
```

---

# SECTION 13 — ADVANCED requests CONCEPTS

## UPLOADING FILES

```python
import requests

# Upload a single file
with open("resume.pdf", "rb") as f:
    files = {"file": f}
    response = requests.post(
        "https://httpbin.org/post",
        files=files
    )
print(response.status_code)

# Upload with additional form data
with open("photo.jpg", "rb") as f:
    files = {"photo": ("profile.jpg", f, "image/jpeg")}
    data  = {"user_id": "42", "type": "profile"}
    response = requests.post(url, files=files, data=data)
```

---

## HANDLING PAGINATION

Many APIs return data in pages. You must fetch all pages.

```python
import requests

def get_all_repos(username: str) -> list:
    """Fetch all public repos for a GitHub user, handling pagination."""
    all_repos = []
    page = 1
    per_page = 100   # Maximum GitHub allows

    while True:
        url = f"https://api.github.com/users/{username}/repos"
        params = {"page": page, "per_page": per_page, "sort": "updated"}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        repos = response.json()
        if not repos:
            break   # No more pages

        all_repos.extend(repos)
        page += 1

        # Check if there are more pages via Link header
        link_header = response.headers.get("Link", "")
        if 'rel="next"' not in link_header:
            break

    return all_repos

repos = get_all_repos("torvalds")
print(f"Total repos: {len(repos)}")
```

---

## CACHING RESPONSES

For data that doesn't change often, cache locally:

```python
import requests
import json
import os
import time

def get_with_cache(url: str, cache_file: str, ttl_seconds: int = 3600) -> dict:
    """
    Fetch URL but cache the response locally.
    Returns cached data if it's fresh (within ttl_seconds).
    """
    # Check if cache file exists and is fresh
    if os.path.exists(cache_file):
        file_age = time.time() - os.path.getmtime(cache_file)
        if file_age < ttl_seconds:
            print(f"📦 Using cached data ({int(file_age)}s old)")
            with open(cache_file, "r") as f:
                return json.load(f)

    # Cache miss or expired — fetch fresh data
    print("🌐 Fetching fresh data from API...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    # Save to cache
    with open(cache_file, "w") as f:
        json.dump(data, f, indent=2)

    return data

# First call: fetches from API
data = get_with_cache(
    "https://api.github.com/users/Adyaprana",
    "cache_adyaprana.json",
    ttl_seconds=3600   # Cache for 1 hour
)
print(data["name"])

# Second call within 1 hour: uses cache (instant)
data = get_with_cache(
    "https://api.github.com/users/Adyaprana",
    "cache_adyaprana.json",
    ttl_seconds=3600
)
print(data["name"])
```

---

# SECTION 14 — INTERVIEW QUESTIONS (ADVANCED)

## Q1. What is the `requests` library and why is it preferred over `urllib`?

The `requests` library is a third-party Python HTTP library created by Kenneth Reitz in 2011. It's nicknamed "HTTP for Humans" because it dramatically simplifies making HTTP requests compared to Python's built-in `urllib` module.

`urllib` is verbose, requires manual encoding of parameters, manual handling of redirects, and manual JSON parsing. It also has inconsistent interface changes between Python 2 and 3.

`requests` provides a clean, consistent API: `requests.get(url)`, `requests.post(url, json=data)`. It handles redirects automatically, encodes parameters automatically, parses JSON with `.json()`, and manages connection pooling internally via urllib3 (which it wraps). The code is readable, minimal, and intuitive — following Python's principle of readability.

Internally, `requests` uses `urllib3` for connection management, which implements HTTP/1.1 keep-alive connections, SSL/TLS, and connection pools. When you use a `Session`, requests reuses the underlying TCP connection (persistent connections), making multiple requests to the same host significantly faster than opening a new connection each time.

---

## Q2. What is the difference between `response.text`, `response.content`, and `response.json()`?

All three access the response body, but in different forms:

**`response.content`** returns the raw response body as **bytes** (`bytes` type). This is the actual bytes received from the server before any decoding. Use this when downloading binary files: images, PDFs, zip files, or any binary data.

```python
with open("image.jpg", "wb") as f:
    f.write(response.content)
```

**`response.text`** decodes `response.content` to a **string** (`str` type) using the encoding detected from the response headers (or chardet if no charset is specified). Use this when working with HTML pages or plain text responses.

```python
html = response.text   # String, already decoded
```

**`response.json()`** calls `json.loads(response.text)` (or `response.content.decode()`) to parse the JSON string and return a **Python object** (dict or list). Use this for all JSON API responses. It raises `json.JSONDecodeError` if the response is not valid JSON.

```python
data = response.json()   # Dict or list
```

**Order of preference:** For REST API responses → `.json()`. For file downloads → `.content`. For HTML/text responses → `.text`.

---

## Q3. What does `response.raise_for_status()` do and when should you use it?

`raise_for_status()` raises an `HTTPError` exception if the response status code indicates a failure — specifically, any 4xx or 5xx status code.

Without it:

```python
response = requests.get("https://api.example.com/users/99999")
# status_code = 404 but NO exception is raised
data = response.json()   # Might get error JSON, not user data
# Silent failure — you might use wrong data without knowing
```

With it:

```python
response = requests.get("https://api.example.com/users/99999")
response.raise_for_status()   # Raises HTTPError for 404
# Code below never runs if request failed
data = response.json()
```

The raised `HTTPError` contains the original response:

```python
except requests.exceptions.HTTPError as e:
    print(e.response.status_code)    # 404
    print(e.response.json())         # {"error": "User not found"}
```

**When to use it:** Always use it in production code. The alternative is checking `response.status_code` manually for every possible error code. `raise_for_status()` followed by a single `except HTTPError` is cleaner and catches all HTTP errors in one place.

---

## Q4. What is connection pooling in requests.Session() and why does it matter for performance?

When you call `requests.get(url)`, Python creates a TCP connection, sends the request, receives the response, and by default may close the connection. For a single request, this is fine. For multiple requests to the same server, it becomes expensive.

Each TCP connection establishment involves:
1. DNS resolution (10-100ms)
2. TCP three-way handshake (1 round trip)
3. TLS handshake for HTTPS (1-2 round trips)

For 10 API calls to the same server without session: 10 × (DNS + TCP + TLS) overhead.

`requests.Session()` uses **urllib3's connection pool** internally. After the first connection to a server is established, it's kept open in the pool (HTTP keep-alive). Subsequent requests to the same server reuse the existing connection, skipping DNS, TCP, and TLS overhead.

```python
# Without Session: 10 TCP connections, 10 TLS handshakes
for user_id in range(1, 11):
    requests.get(f"https://api.github.com/users/{user_id}")

# With Session: 1 TCP connection, 1 TLS handshake, 10 requests
with requests.Session() as session:
    for user_id in range(1, 11):
        session.get(f"https://api.github.com/users/{user_id}")
```

For 10 GitHub API calls, the Session version can be 2-5x faster due to eliminated connection overhead. The improvement is larger for HTTPS APIs (TLS handshake is expensive) and for high-latency networks.

---

## Q5. How do you handle rate limiting when calling external APIs?

Rate limiting is when an API restricts how many requests you can make in a time period. Common responses: 429 Too Many Requests.

**Strategy 1: Respect Retry-After header**

```python
import time
import requests

def get_with_rate_limit_handling(url: str, max_retries: int = 3) -> dict | None:
    for attempt in range(max_retries):
        response = requests.get(url, timeout=10)

        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))
            print(f"Rate limited. Waiting {retry_after} seconds...")
            time.sleep(retry_after)
            continue

        response.raise_for_status()
        return response.json()

    return None
```

**Strategy 2: Exponential backoff**

```python
import time

def get_with_backoff(url: str, max_retries: int = 5) -> dict | None:
    for attempt in range(max_retries):
        response = requests.get(url, timeout=10)

        if response.status_code in (429, 500, 502, 503, 504):
            wait = 2 ** attempt   # 1, 2, 4, 8, 16 seconds
            print(f"Attempt {attempt+1} failed. Waiting {wait}s...")
            time.sleep(wait)
            continue

        response.raise_for_status()
        return response.json()

    return None
```

**Strategy 3: Check rate limit headers proactively**

GitHub API includes `X-RateLimit-Remaining`. Check before you hit zero:

```python
response = requests.get(url)
remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
reset_time = int(response.headers.get("X-RateLimit-Reset", 0))

if remaining < 5:
    wait = reset_time - time.time()
    if wait > 0:
        print(f"Low rate limit. Sleeping {wait:.0f}s...")
        time.sleep(wait)
```

---

## Q6. When should you use `requests` vs `httpx` vs `aiohttp`?

All three are HTTP clients for Python. The choice depends on your context:

**`requests` (synchronous):**

```
Use when:
  → Scripts, CLI tools, data pipelines
  → Synchronous Flask or Django (not FastAPI)
  → Simple one-off API calls
  → Learning and prototyping

Don't use when:
  → You need concurrent requests (use gather with httpx instead)
  → You're in an async FastAPI endpoint
```

**`httpx` (sync + async):**

```
Use when:
  → FastAPI async endpoints (await httpx.AsyncClient().get())
  → You want both sync and async from same library
  → HTTP/2 support needed
  → Drop-in replacement for requests with async capability

pip install httpx
```

```python
# Sync (same as requests)
response = httpx.get(url)

# Async (in FastAPI/asyncio)
async with httpx.AsyncClient() as client:
    response = await client.get(url)
```

**`aiohttp` (async only):**

```
Use when:
  → High-performance async HTTP client
  → WebSocket support needed
  → You're already using aiohttp server

pip install aiohttp
```

**For your backend development journey:**

```
Learning scripts → requests
FastAPI endpoints → httpx (async)
Performance-critical → aiohttp or httpx
```

---

# DAY 26 ASSIGNMENTS

✅ Install the `requests` library and verify: `import requests; print(requests.__version__)`

✅ Make a GET request to `https://api.github.com/users/octocat` and print name, followers, repos

✅ Write the GitHub Profile Fetcher (Simple Version) and test with your own username

✅ Test error handling: request a non-existent user and verify the 404 handling works

✅ Make a POST request to `https://httpbin.org/post` with your name and print what the server echoes back

✅ Add `timeout=5` to all your requests and verify it compiles

✅ Try calling `https://httpbin.org/delay/10` with `timeout=2` and catch the Timeout exception

✅ Get a free API key from openweathermap.org and test the Weather Fetcher

✅ Use `requests.Session()` to make 3 requests to the same API host

✅ Write the `safe_get()` wrapper function and use it in two places

✅ Try `response.raise_for_status()` with a 404 URL and print the exception

---

# DAY 26 BACKEND DEVELOPER CHECKPOINT

If you can explain without notes:

**Core Concepts:**
✅ What `requests` is and why it exists (HTTP for Humans)
✅ What a Response object contains (.status_code, .text, .json(), .headers)
✅ All status code families: 2xx success, 4xx client error, 5xx server error
✅ The difference between `.text`, `.content`, and `.json()`

**Making Requests:**
✅ `requests.get(url, params=..., headers=..., timeout=...)`
✅ `requests.post(url, json=..., headers=..., timeout=...)`
✅ `requests.put()`, `.patch()`, `.delete()`
✅ Why to use `params=` dict instead of building URL manually

**Professional Patterns:**
✅ Always pass `timeout=` — never leave it out
✅ `response.raise_for_status()` — what it does and when to use it
✅ Full try/except pattern for all requests exceptions
✅ `requests.Session()` — when and why to use it
✅ The `safe_get()` wrapper pattern

**Projects:**
✅ GitHub Profile Fetcher — accessing nested JSON data
✅ Weather Fetcher — query params, API keys in headers, nested JSON
✅ Error handling for 404, 401, 429 status codes

---

Tomorrow when you call an external API from your FastAPI backend:

```python
@app.get("/github/{username}")
async def get_github_user(username: str):
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://api.github.com/users/{username}",
            timeout=10
        )
    response.raise_for_status()
    return response.json()
```

You'll understand exactly what every line does:

```
httpx.AsyncClient()          → async version of requests.Session()
await client.get()           → non-blocking HTTP GET
timeout=10                   → never hang forever
raise_for_status()           → raise exception if 4xx or 5xx
response.json()              → parse JSON to Python dict
```

**That's the difference between copying code from Stack Overflow and knowing exactly why it works.**

---

## 🎥 Recommended Learning Video

> **✅ Corey Schafer: Python Requests Library (English)**
>
> Corey Schafer is one of the best Python educators on YouTube.
> His Requests tutorial is clear, practical, and covers real examples.
>
> Watch it. Practice alongside it.
> Then build the GitHub Fetcher and Weather Fetcher from this file.

---

*Day 26 Complete.* ✅