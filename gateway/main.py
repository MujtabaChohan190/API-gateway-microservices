#fast api - middleware - routers - exception handlers - startup event
from fastapi import FastAPI , Request
from router import router
import httpx
import time

app = FastAPI(title= "API GATEWAY")

@app.middleware("http")
async def log_requests(request : Request, call_next):
    start_time = time.time()
    #passing the request to endpoint - gateway router
    response = await call_next(request)
    #now we had received the resposne from endpoint 
    end_time = time.time()
    process_time = end_time - start_time

    print(
        f"[{request.method}] {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Duration:{process_time:.4f}s"
    )

    return response #  Passing the intercepted response back to the client to complete the request

app.include_router(router)


