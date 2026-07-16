# this file holds actual gateway logic 
#router : extracts service name , build target url for dynamic endpoints and return it

from fastapi import APIRouter, HTTPException, Request , Response
import httpx

from config import SERVICES

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
    if service not in SERVICES:
        raise HTTPException(
            status_code=404,
            detail=f"Service '{service}' not found.",
        )

    base_url = SERVICES[service]
    target_url = f"{base_url}/{path}"

    async with httpx.AsyncClient() as client:
        # Client sends http request , API gateway catches that incoming detail and creates a new outgoing request using client.request
        # Forward everything (headers, query params, and request body) to the microservice
        try:
            response = await client.request(
                method=request.method,
                url=target_url,
                headers=dict(request.headers),
                params=dict(request.query_params),  
                content=await request.body(),  
                timeout=5.0     
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

    #once that request is forwarded , backend microservices processes data and save to db - it returns the raw data to gateway
    # Gateway returns the clean microservice response back to the client
    return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
    )