from fastapi import FastAPI
from router import router
import httpx

app = FastAPI(title= "API GATEWAY")
app.include_router(router)


