# FastAPI Fundamentals 

# Part 1 — What is a Web Framework?
# Before FastAPI existed
# If someone visited -> https://example.com/users

# who receives that request -> Python, The operating system, The browser No.
# Something has to:
# listen on a port
# accept TCP connections
# parse HTTP
# route URLs
# create responses
# That "something" is a web server and a web framework.




# Part 2 — The Journey of an HTTP Request

# We'll trace one request from start to finish.
# Browser -> DNS -> IP Address -> TCP Connection -> HTTP Request -> Uvicorn -> FastAPI -> Your Function -> JSON Response -> Browser
# This single diagram explains almost the entire backend request lifecycle.




# Part 3 — Why FastAPI Exists
# Before FastAPI there were frameworks like: Flask, Django, Pyramid, Bottle
# FastAPI was built because Python lacked a framework that was simultaneously: fast, asynchronous, type-safe, self-documenting, editor-friendly
# FastAPI achieves this by relying heavily on Python type hints and the ASGI ecosystem.




# Part 4 — What is ASGI?
# Previously we discussed: HTTP -> Server -> Application
# But in Python there's another layer: Client -> HTTP -> Uvicorn -> ASGI -> FastAPI -> Code
# FastAPI doesn't talk directly to sockets.
# Uvicorn handles network communication.
# ASGI defines how servers and applications communicate.




# Part 5 — Why Uvicorn?
# Many beginners think: FastAPI runs my app.
# Not exactly.
# Actually: Browser -> Uvicorn -> FastAPI -> Your endpoint
# Uvicorn is the server.
# FastAPI is the application.
# This distinction becomes important later when we discuss deployment.




# Part 6 — Why Swagger Exists
# When you define: @app.get("/users")
# FastAPI already knows: URL, HTTP method, parameter types, return type
# It can generate API documentation automatically.
# That documentation appears at: /docs
# This is one of FastAPI's biggest productivity advantages.




# Part 7 — Path vs Query Parameters
# We'll understand the concept before writing code.

# Path Parameter -> /users/25
# Meaning: Give me user 25.

# The value identifies a specific resource.
# Query Parameter -> /users?limit=10
# Meaning: Give me users, but only 10.
# It modifies how the request behaves rather than identifying a resource.

# Later you'll see combinations like:
# /users/25/orders?limit=5&page=2
# and understand exactly what each part does.


