# 🚀 Backend Developer Journey — Project 1 (URL Shortener API)

# Day 56 — First API Endpoint

# Let's see where we are
# Over the last 7 days, we've built each layer independently.

# Database Layer        ✅
# Model Layer           ✅
# Schema Layer          ✅
# Repository Layer      ✅
# Service Layer         ✅

# Today we're building the final missing layer: Router Layer          ⏳

# The Project Architecture 
# This is the complete request flow this project achieve today: Client -> POST /shorten -> URLCreate (Schema) -> Router -> URLService -> URLRepository -> PostgreSQL -> URLResponse (Schema) -> Client
# When this works, you've successfully built your first complete layered backend request.


# Why do we need a Router?
# Imagine we didn't have one. 
# We could write: app.post("/shorten")
# directly inside main.py. Would it work -> Yes.

# But now imagine after Version 2.
# We add: POST /login, POST /register, GET /users, PUT /users/{id}, DELETE /users/{id}, POST /admin/login, GET /analytics, POST /qr, GET /stats, GET /health, 
# Now imagine all of those endpoints inside: main.py
# It becomes: 2000+ lines -> Finding one endpoint becomes difficult.


# Professional Projects split endpoints by feature.
# Example:
# routers/
#     url_router.py
#     auth_router.py
#     user_router.py
#     analytics_router.py

# Then: main.py
# only connects them together. Much cleaner.


# Responsibilities
# Let's lock in the final responsibility chart.
# | Layer      | Responsibility                |
# | ---------- | ----------------------------- |
# | Router     | HTTP Requests & Responses     |
# | Service    | Business Logic                |
# | Repository | Database Operations           |
# | Model      | Database Structure            |
# | Schema     | Request & Response Validation |
# This table is worth remembering. It comes up in interviews and real code reviews.


# Today's Build Plan
# We'll take it one step at a time.

# Create Router
#         ↓
# Create POST /shorten
#         ↓
# Inject Database Session
#         ↓
# Call Service
#         ↓
# Return Response
#         ↓
# Register Router
#         ↓
# Test in Swagger


# One Design Decision Before We Start This is another architecture decision.
# Inside routers/, should we create:
# Option A -> url.py
# Option B -> url_router.py

# My Recommendation -> url_router.py
# Reason: As the project grows, you'll have: models/url.py, schemas/url.py, services/url_service.py, repositories/url_repository.py, routers/url_router.py
# Every file has a clear purpose just from its name. No confusion.


# First Task of Day 56
# Create:
# app/
# └── routers/
#       └── url_router.py
# Don't write any code yet.


# Today is a Special Day 
# If everything goes well, by the end of today's session you'll be able to open: http://127.0.0.1:8000/docs
# Click POST /shorten, send:
# {
#     "original_url": "https://google.com"
# }
# and receive:
# {
#     "id": 1,
#     "original_url": "https://google.com",
#     "short_code": "Ab12Cd",
#     "short_url": "http://127.0.0.1:8000/Ab12Cd"
# No temporary scripts, No manual object creation, A real REST API.
# This is one of the biggest milestones in the entire project because it's the first time every layer you've built over the last week will work together as a single application.





# Step 1 — Create url_router.py
# Inside:
# app/
# └── routers/
#       └── url_router.py

# Write only the imports first.

# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database.database import get_db
# from app.schemas.url import URLCreate, URLResponse
# from app.services.url_service import URLService

# Why these imports?
# Very quickly:

# APIRouter → Creates routes.
# Depends → Gives us the database session.
# Session → Type hint.
# get_db → Opens and closes the database session automatically.
# URLCreate → Request body.
# URLResponse → Response body.
# URLService → Business logic.
# Nothing more.





# Step 2 — Create the Router
# router = APIRouter(
#     prefix="/shorten",
#     tags=["URL Shortener"]
# )
# Why prefix -> Without it: POST /
# With it: POST /shorten
# Much cleaner.

# Why tags -> Swagger groups endpoints.
# Instead of showing a random list, you'll see: 
# URL Shortener
#     POST /shorten
# Later we'll add: Authentication, Users, Analytics
# Each group stays organized.







# Step 3 — Create the Endpoint
# Below the router, write this:

# @router.post(
#     "",
#     response_model=URLResponse,
#     status_code=201
# )
# def create_short_url(
#     url: URLCreate,
#     db: Session = Depends(get_db)
# ):
#     service = URLService()

#     return service.create_short_url(
#         db=db,
#         original_url=str(url.original_url)
#     )

# 1. @router.post("")
# Remember we already set: prefix="/shorten" So: @router.post("") means: POST /shorten
# If we wrote: @router.post("/create") then it would become: POST /shorten/create

# 2. response_model=URLResponse
# FastAPI will automatically convert our SQLAlchemy object into this schema.
# Flow: Database Result → URLResponse (Schema) → JSON → Client

# 3. status_code=201 201 means: Resource Created Not: 200 OK
# Creating a resource should return 201 Created. This is a REST API best practice.

# 4. db: Session = Depends(get_db)
# This is FastAPI's Dependency Injection. You already know what get_db() does.
# Flow: Request Starts → Create Session → Use Session → Automatically Close Session
# No need to manually write: db = SessionLocal() or db.close() FastAPI handles it.

# 5. str(url.original_url)
# Remember: original_url: HttpUrl inside our schema?
# HttpUrl is a Pydantic type, not a plain Python string.
# Our Service expects: original_url: str
# So we convert it using: str(...)

# Before this endpoint can work, our Service needs a small change. Right now it returns a ShortenedURL model, but URLResponse expects:
{
    "id": 1,
    "original_url": "...",
    "short_code": "...",
    "short_url": "..."
}
# Our model doesn't have short_url. We'll fix that in the next step by updating the Service to build the response correctly.


# Full Code Of url_router.py :
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database.database import get_db
# from app.schemas.url import URLCreate, URLResponse
# from app.services.url_service import URLService

# router = APIRouter(
#     prefix="/shorten",
#     tags=["URL Shortener"]
# )
# @router.post(
#     "",
#     response_model=URLResponse,
#     status_code=201
# )
# def create_short_url(
#     url: URLCreate,
#     db: Session = Depends(get_db)
# ):
#     service = URLService()
#     return service.create_short_url(
#         db=db,
#         original_url=str(url.original_url)
#     )




# Now let's go through the url_router.py line by line.


# from fastapi import APIRouter, Depends

# APIRouter ->This class is used to create a group of related API endpoints.
# Think of it like this:
# FastAPI App/
#     │
#     ├── URL Router
#     ├── User Router
#     ├── Auth Router
#     └── Admin Router
# Instead of putting every endpoint inside main.py, we organize them into routers.

# Depends  -> Depends is FastAPI's Dependency Injection system.
# It tells FastAPI: "Before calling my function, give me this dependency."
# In our case: db: Session = Depends(get_db)
# means: "FastAPI, before running this endpoint, call get_db() and give me the database session."


# from sqlalchemy.orm import Session

# We import the SQLAlchemy Session class.
# We're not creating a session here. We're only using it as a type hint.
# db: Session means: "db is expected to be a SQLAlchemy Session object."


# from app.database.database import get_db

# This imports our dependency function.
# Remember we wrote it earlier.
# Its job is:
# Request Starts
#       ↓
# Create Session
#       ↓
# Give Session to Endpoint
#       ↓
# Endpoint Finishes
#       ↓
# Close Session Automatically
# This is why we don't write: db = SessionLocal()
# inside every endpoint.


# from app.schemas.url import URLCreate, URLResponse

# We're importing two Pydantic schemas. URLCreate -> Used for the request body.
# Example:
# {
#     "original_url": "https://google.com"
# }
# FastAPI validates this before our function runs.
# URLResponse -> Used for the response body. Whatever we return,
# FastAPI converts it into this schema before sending it back to the client.


# from app.services.url_service import URLService

# We're importing our Service. Remember its responsibility.
# Router → Receives Request
#        ↓
# Service → Business Logic
# The Router never talks directly to the Repository.



# Creating the Router
# router = APIRouter()
# Here we're creating a new router object.
# Think of it like: app = FastAPI() creates the application. Similarly, router = APIRouter() creates a router.


# prefix="/shorten",
# Every endpoint inside this router automatically starts with: /shorten
# So later: @router.post("") becomes POST /shorten
# And if we add: @router.get("/{short_code}") it becomes: GET /shorten/{short_code}
# The prefix is automatically added. tags=["URL Shortener"]
# This only affects Swagger UI. Instead of a random list of endpoints,
# Swagger groups them like:
# URL Shortener
#     POST /shorten
#     GET /shorten/{short_code}
#     GET /shorten/stats/{short_code}
# It improves documentation.



# Endpoint
# @router.post( -> This is a Python decorator.
# It tells FastAPI: "The function below handles HTTP POST requests."
# "",
# Because we already have: prefix="/shorten"
# an empty string means: POST /shorten
# If we wrote: "/create"
# the endpoint would become: POST /shorten/create
# response_model=URLResponse,
# This tells FastAPI: "Whatever this function returns, convert it into a URLResponse."
# Even if our Service returns a SQLAlchemy model,
# FastAPI uses: model_config = ConfigDict(from_attributes=True)
# to convert it automatically. status_code=201
# HTTP status codes have meanings.
# 200 → OK
# 201 → Created
# 400 → Bad Request
# 404 → Not Found
# 500 → Internal Server Error
# Since this endpoint creates a new shortened URL, 201 Created is the correct REST status code.
# )


# def create_short_url(
# We're defining the endpoint function.
# The function name is for Python. The HTTP endpoint is still: POST /shorten -> url: URLCreate This is the request body. 
# FastAPI automatically: Reads the JSON, Validates it using URLCreate, Creates a Python object.
# Example:
# Client sends:
# {
#     "original_url": "https://google.com"
# }
# Inside our function,
# url becomes:
# URLCreate(
#     original_url=HttpUrl("https://google.com")
# )
# db: Session = Depends(get_db)
# This tells FastAPI: "Before calling this function, execute get_db() and pass its result into db."
# So we don't manually create or close the session.FastAPI does it.
# ):
# End of the function parameters.


# service = URLService()
# We create an instance of our Service. The Router does not contain business logic. Instead, it delegates work to the Service.
# return service.create_short_url(
# Instead of writing business logic here, the Router says: "Service, please create the shortened URL."
# This keeps the Router small and focused.
# db=db, We're passing the database session to the Service.
# The Service needs it because it eventually calls the Repository.
# original_url=str(url.original_url)
# Remember: url.original_url is a Pydantic HttpUrl object.
# Our Service expects a normal Python string.
# So we convert it.
# Example: HttpUrl("https://google.com")
#         ↓
# "https://google.com"
# )
# End of the function call.


# Complete Request Flow
# Now the request flows like this:
# Client → POST /shorten → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL → URLResponse (Schema) → Client






# Only 2 tasks are left:
# ✅ Update URLService
# ✅ Register the router in main.py
# ✅ Run Swagger and test
# Let's do them one by one.

# Step 1 — Update URLService
# Right now your service probably returns: return self.repository.create(db, url)
# That won't work because our router expects: response_model=URLResponse
# And URLResponse contains: id, original_url, short_code, short_url
# But the SQLAlchemy model doesn't have: short_url
# We have two possible approaches
# Option 1 (Quick Fix) -> Return a dictionary.
# Option 2 (Professional) -> Return a URLResponse object.

# We'll use Option 2.
# First Import  
# At the top of url_service.py, add: from app.schemas.url import URLResponse

# Now replace the last part of create_short_url()
# Replace: return self.repository.create(db, url)
# with: 
# saved_url = self.repository.create(db, url)
# return URLResponse(
#     id=saved_url.id,
#     original_url=saved_url.original_url,
#     short_code=saved_url.short_code,
#     short_url=f"http://127.0.0.1:8000/{saved_url.short_code}"
# )


# Let's understand every line

# saved_url = self.repository.create(db, url)
# Previously we returned directly. Now we first store the returned object.
# Why -> Because we need to access: saved_url.id, saved_url.short_code, saved_url.original_url to build the response.
# return URLResponse( -> We're creating a Pydantic response object. This object will be converted into JSON by FastAPI.
# id=saved_url.id, -> The database generated this ID. We're simply returning it.
# original_url=saved_url.original_url, -> The original URL stored in PostgreSQL. 
# short_code=saved_url.short_code, -> # The random code generated by the Service.
# short_url=f"http://127.0.0.1:8000/{saved_url.short_code}" -> This is the complete shortened URL.
# If: short_code = Ab12Cd Then: http://127.0.0.1:8000/Ab12Cd



# Why build short_url here Why not store it in PostgreSQL?
# Because: short_url = Base URL + short_code
# The database already stores: short_code
# The base URL may change:
# Development: http://127.0.0.1:8000
# Production: https://myurlshortener.com
# Staging: https://staging.myurlshortener.com
# If we stored the full URL in the database, we'd have to update every row whenever the domain changed.
# Instead, we generate it dynamically. Much better design.



# 🎯 Task 2 — Register the Router
# Open main.py.
# At the top add: from app.routers.url_router import router as url_router

# Then after: app = FastAPI(...)
# add: app.include_router(url_router)


# What does this line do -> app.include_router(url_router)
# FastAPI says: "Take every endpoint inside url_router and add it to my application."
# Without this line: POST /shorten doesn't exist.
# Even though we wrote the file. This is exactly like the model registration we did earlier.
# Remember: from app.models.shortened_url import ShortenedURL
# We imported the model so SQLAlchemy could register it.
# Now: app.include_router(...)
# registers the router with FastAPI.


# Yesterday:
# Python Script → Repository → PostgreSQL

# Today:
# Client → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL → URLResponse (Schema) → Client


# The Project have officially built your first complete backend endpoint.
# Look at what accomplished:
# ✅ Client sent an HTTP request.
# ✅ FastAPI validated it using URLCreate.
# ✅ Router received it.
# ✅ Service generated a unique short code.
# ✅ Repository saved it.
# ✅ PostgreSQL stored it.
# ✅ Service created the response.
# ✅ FastAPI returned JSON.
# That's an end-to-end request lifecycle.

# Why is redirect not working?
# when opened: http://127.0.0.1:8000/LLMaWS
# and got:
# {
#     "detail": "Not Found"
# }
# This is 100% expected. There is no bug.
# Let's see why. Right now your application only has: GET / and POST /shorten
# That's it.
# When the browser requests: GET /LLMaWS
# FastAPI searches for: @app.get("/{short_code}")
# Does it exist -> No. So FastAPI replies: 404 Not Found Exactly what it should do.

# current application:
# Client → POST /shorten → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL → URLResponse (Schema) → Client
# Works perfectly. But this route: GET /{short_code} doesn't exist yet.

# What's missing RThe original roadmap -> wanted three endpoints.
# ✅ Completed
# POST /shorten
# ⏳ Next GET /{short_code}

# Client → Router → URLService → URLRepository → PostgreSQL → RedirectResponse → Browser
# This endpoint will:
# Receive: LLMaWS -> Search PostgreSQL -> Find: https://chatgpt.com/ -> Increment click count -> Redirect the browser

