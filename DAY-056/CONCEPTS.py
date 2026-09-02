# ============================
# DAY 56 - IMPORTANT CONCEPTS
# ============================

# 1. What is a Router?
# Answer: A Router groups related API endpoints together.
# Instead of writing every endpoint in main.py, we organize them into separate router files.
# Example:
# routers/
#     url_router.py
#     auth_router.py
#     user_router.py

# 2. Why do we use APIRouter?
# Answer: APIRouter helps organize endpoints by feature.
# It makes the project modular, easier to maintain, and keeps main.py clean.

# 3. What does the Router know?
# The Router knows:
# - HTTP Requests
# - HTTP Responses
# - FastAPI Dependencies
# - Pydantic Schemas
# - Services
#
# The Router should NOT know:
# - SQL Queries
# - Database Logic
# - Business Rules

# 4. What is Dependency Injection (Depends)?
# Answer: Dependency Injection allows FastAPI to automatically provide required objects.
# In our project:
# Request Starts → get_db() → Database Session → Endpoint → Session Closed Automatically

# 5. Why do we use response_model?
# Answer: response_model tells FastAPI how the response should look.
# It validates and converts the returned object into the expected JSON format.

# 6. Why do we use status_code=201?
# Answer: HTTP 201 means "Resource Created".
# Since POST /shorten creates a new resource, returning 201 follows REST API standards.

# 7. Why convert HttpUrl to str?
# Answer: URLCreate stores original_url as a Pydantic HttpUrl object.
# Our Service expects a normal Python string.
# So:
# HttpUrl("https://google.com")
#            ↓
# "https://google.com"

# 8. Why is short_url not stored in the database?
# Answer: short_url = Base URL + short_code
# Since the base URL changes between Development, Staging, and Production,
# we generate it dynamically instead of storing it.

# Example:
# Development → http://127.0.0.1:8000/Ab12Cd
# Production  → https://myurlshortener.com/Ab12Cd

# 9. What does app.include_router() do?
# Answer: It registers all endpoints inside a router with the FastAPI application.
# Without it, FastAPI doesn't know the router exists.

# Flow:
# app.include_router(url_router)
#             ↓
# POST /shorten becomes available

# 10. Current Request Flow
# Client → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL → URLResponse (Schema) → Client




# ============================
# DAY 56 - INTERVIEW QUESTIONS
# ============================

# 1. What is APIRouter in FastAPI?
# Answer:
# APIRouter is used to group related API endpoints into separate modules,
# making the project modular and maintainable.

# 2. Why shouldn't we put all endpoints inside main.py?
# Answer:
# As the application grows, main.py becomes difficult to read and maintain.
# Routers separate features into independent modules.

# 3. What is the responsibility of the Router layer?
# Answer:
# The Router handles HTTP requests, validates input using Pydantic schemas,
# calls the Service layer, and returns HTTP responses.

# 4. What is Dependency Injection in FastAPI?
# Answer:
# Dependency Injection automatically provides required objects to an endpoint,
# such as a database session using Depends(get_db).

# 5. What is the purpose of response_model?
# Answer:
# response_model validates, filters, and formats the API response before sending it to the client.

# 6. Why do we use HTTP Status Code 201 instead of 200?
# Answer:
# 201 indicates that a new resource has been successfully created,
# while 200 simply indicates a successful request.

# 7. Why is short_url generated dynamically?
# Answer:
# Because the base domain changes between environments.
# Only short_code is stored in the database.
# short_url is built when sending the response.

# 8. Why doesn't the Router talk directly to the Repository?
# Answer:
# The Router should only handle HTTP communication.
# Business logic belongs to the Service layer.
# Database operations belong to the Repository layer.

# Correct Flow:
# Client → URLCreate (Schema) → Router → URLService → URLRepository → PostgreSQL → URLResponse (Schema) → Client

# 9. What happens when a client sends POST /shorten?
# Answer:
# FastAPI validates the request using URLCreate,
# passes it to the Router,
# the Router calls the Service,
# the Service generates a unique short code,
# the Repository saves it,
# PostgreSQL stores it,
# and the response is returned as URLResponse.

# 10. What milestone did we achieve today?
# Answer:
# We built our first complete end-to-end REST API endpoint.
# The request now flows through every layer of the application:
# Client → Router → Service → Repository → Database → Client.