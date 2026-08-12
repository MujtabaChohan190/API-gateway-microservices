# API Gateway with FastAPI

A dynamic API Gateway built from scratch using **FastAPI, HTTPX, JWT, Redis, and multiple microservices**.

This project demonstrates how an API Gateway can act as a centralized entry point between clients and backend microservices while handling authentication, routing, caching, rate limiting, request forwarding, and error handling.

## Architecture

```text
                         CLIENT
                           │
                           ▼
                    ┌─────────────┐
                    │ API Gateway │
                    │    :8000    │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
       JWT Auth          Redis        Rate Limiting
          │                │                │
          └────────────────┼────────────────┘
                           │
                    Dynamic Routing
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
        Auth :8003    Products :8002   Users :8001
```

## Features

* **Dynamic Request Routing** — Routes requests to different microservices using a service registry.
* **HTTP Request Forwarding** — Supports GET, POST, PUT, PATCH, and DELETE requests.
* **JWT Authentication** — Authentication is centralized at the gateway.
* **Redis Caching** — Frequently requested GET responses are cached using Redis.
* **Cache Invalidation** — Successful write operations invalidate cached GET responses.
* **Rate Limiting** — Implements fixed-window rate limiting using Redis.
* **CORS** — Configured for cross-origin requests.
* **Request Logging** — Logs HTTP method, endpoint, status code, and processing time.
* **Error Handling** — Handles service timeouts, unavailable services, and unexpected exceptions.
* **Header Filtering** — Removes hop-by-hop HTTP headers before forwarding requests.

## Tech Stack

| Technology        | Purpose                       |
| ----------------- | ----------------------------- |
| Python            | Backend development           |
| FastAPI           | API Gateway and microservices |
| HTTPX             | HTTP request forwarding       |
| Redis             | Caching and rate limiting     |
| JWT               | Authentication                |
| Pydantic Settings | Configuration management      |
| Uvicorn           | ASGI server                   |
| Docker            | Redis container               |

## Project Structure

```text
api_gateway_project/
│
├── auth_service/
│   ├── config.py
│   └── main.py
│
├── gateway/
│   ├── auth.py
│   ├── config.py
│   ├── exception_handler.py
│   ├── main.py
│   ├── rate_limiter.py
│   ├── redis_client.py
│   └── router.py
│
├── product_service/
│   └── main.py
│
├── user_service/
│   └── main.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## How Request Routing Works

The gateway uses a dynamic catch-all route:

```text
/{service}/{path:path}
```

For example:

```text
GET /products/products
```

is received by the gateway and translated into:

```text
http://127.0.0.1:8002/products
```

The gateway therefore does not need a separate route for every backend endpoint.

The service registry determines where each request should be sent:

```python
SERVICES = {
    "users": "...",
    "products": "...",
    "auth": "..."
}
```

## Authentication Flow

Authentication is centralized at the gateway.

```text
Client
  │
  │ POST /auth/login
  ▼
Gateway
  │
  ▼
Auth Service
  │
  ▼
JWT Token
  │
  ▼
Client
```

For protected endpoints:

```text
Client
  │
  │ Authorization: Bearer <token>
  ▼
Gateway
  │
  ├── Verify JWT
  ├── Apply rate limit
  ├── Check Redis cache
  │
  ▼
Microservice
```

## Redis Caching

The gateway uses a **cache-aside strategy** for GET requests.

```text
Client
  │
  ▼
Gateway
  │
  ▼
Redis
  │
  ├── HIT ──────► Return cached response
  │
  └── MISS
        │
        ▼
   Microservice
        │
        ▼
   Store response
        │
        ▼
      Client
```

Successful GET responses are stored in Redis using a configurable TTL.

## Cache Invalidation

When a successful write operation occurs:

```text
POST / PUT / PATCH / DELETE
          │
          ▼
    Microservice
          │
          ▼
        Success
          │
          ▼
    Cache invalidated
```

The next GET request retrieves fresh data from the microservice.

## Rate Limiting

The gateway uses Redis to implement a fixed-window rate limiter.

Current configuration:

```text
5 requests
per 60 seconds
```

When the limit is exceeded, the gateway returns:

```text
429 Too Many Requests
```

## Error Handling

The gateway handles common downstream failures:

| Situation                | Response |
| ------------------------ | -------- |
| Unknown service          | 404      |
| Missing/invalid JWT      | 401      |
| Rate limit exceeded      | 429      |
| Microservice timeout     | 504      |
| Microservice unavailable | 503      |
| Unexpected gateway error | 500      |

## Running the Project

### 1. Create and activate the virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create the required `.env` files using `.env.example` as a reference.

Do not commit real `.env` files or secret keys to GitHub.

### 4. Start Redis

The project uses Redis running on:

```text
localhost:6379
```

### 5. Start the microservices

Auth service:

```bash
uvicorn auth_service.main:app --reload --port 8003
```

Product service:

```bash
uvicorn product_service.main:app --reload --port 8002
```

User service:

```bash
uvicorn user_service.main:app --reload --port 8001
```

### 6. Start the API Gateway

```bash
uvicorn gateway.main:app --reload --port 8000
```

The API Gateway will then be available at:

```text
http://127.0.0.1:8000
```

## Testing

The project was tested end-to-end using Postman.

The following functionality was verified:

* JWT login and token generation
* Authenticated requests
* Dynamic routing
* Redis cache MISS and HIT
* Cache invalidation
* Rate limiting
* `429 Too Many Requests`
* CORS preflight requests
* Microservice communication
* Gateway error handling

## Example Request

Authenticated product request:

```http
GET /products/products
Authorization: Bearer <JWT_TOKEN>
```

Example response:

```json
[
    {
        "id": 1,
        "name": "Laptop"
    },
    {
        "id": 2,
        "name": "Phone"
    }
]
```

## What I Learned

This project was built to understand how backend systems can be structured beyond individual REST APIs.

The main concepts explored were:

* Reverse proxy architecture
* Microservice communication
* Dynamic routing
* JWT authentication
* Redis caching
* Cache invalidation
* Rate limiting
* HTTP request forwarding
* Middleware
* Error handling
* Environment-based configuration

## Future Improvements

Potential future improvements include:

* Service health checks
* Circuit breaker pattern
* Better cache key management
* Distributed rate limiting
* Persistent databases for microservices
* Dockerizing the complete system
* Centralized monitoring and metrics
* Automated testing with Pytest
* Service discovery

---

## Project Status

**Completed and end-to-end tested.**

The gateway successfully routes requests between multiple microservices while providing centralized authentication, Redis caching, rate limiting, request logging, CORS handling, and error management.
