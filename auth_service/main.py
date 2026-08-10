from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from jose import jwt
from datetime import datetime, timedelta
from config import settings

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(data: LoginRequest):

    if data.username != "mujtaba" or data.password != "1234":
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    #here we do token payload construction by packaging the user identity
    payload = {
        "sub": data.username,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    #here we encrypt the payload using the secret key and algorithm
    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm= settings.ALGORITHM
    )
    #here we return the signed jwt string along with bearer designation back to client
    return {
        "access_token": token,
        "token_type": "bearer"
    }