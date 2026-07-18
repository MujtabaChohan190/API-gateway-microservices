# this file holds actual gateway logic 
#router : extracts service name , build target url for dynamic endpoints and return it

from fastapi import APIRouter, HTTPException, Request , Response
import httpx
from auth import extract_token, verify_token
from redis_client import redis_client
from config import SERVICES , GATEWAY_TIMEOUT , CACHE_TTL

router = APIRouter()

@router.api_route(
    "/{service}/{path:path}",
    methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
)
async def gateway(
    request: Request,
    service: str,
    path: str,
):
    #Building Target url through service registry as a catch all routes for all endpoints
    if service not in SERVICES:
        raise HTTPException(
            status_code=404,
            detail=f"Service '{service}' not found.",
        )

    base_url = SERVICES[service]
    target_url = f"{base_url}/{path}"

    #JWT Authentication
    auth_header= request.headers.get("Authorization")
    token= extract_token(auth_header)
    verify_token(token)

    #Once verified , before request goes to endpoint , we check at redis cache to see if cache hits 
    cache_key = f"{request.method}:{target_url}?{request.url.query}"
    if request.method == "GET":
        cached_data= await redis_client.get(cache_key)

        if cached_data is not None:
            print("Cache Hit")

            # data is found in cache so we are returning it  - for cache response we have only text , rest we have to give
            return Response(
                content= cached_data,
                status_code=200,
                media_type="application/json"
            )
        print("Cache miss")

    #Not found in cache , fast api now requests from endpoint
    async with httpx.AsyncClient() as client:
        # Client sends http request , API gateway catches that incoming detail and creates a new outgoing request using client.request
        # Forward everything (headers, query params, and request body) to the microservice
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=dict(request.headers), #this forwards every header , host - content length and connection 
                params=dict(request.query_params),  
                content=await request.body(),  
                timeout=GATEWAY_TIMEOUT
            )

        #backend microservice was temporarily unavailable
        except httpx.RequestError:
            raise HTTPException(
                status_code = 503,
                detail = f"{service.capitalize()} Service is currently unavailable"
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code = 504,
                detail = f"{service.capitalize()} Service timed out"
            )
        #HTTPX requests have succeeded , store successful get response in redis
        if request.method == "GET" and response.status_code == 200:
            await redis_client.setex(
                cache_key, 
                CACHE_TTL,
                response.text
            )
    

    #once that request is forwarded , backend microservices processes data and save to db - it returns the raw data to gateway
    # Gateway returns the clean microservice response back to the client
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )