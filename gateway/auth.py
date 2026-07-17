from fastapi import HTTPException, status
from config import SECRET_KEY, ALGORITHM
from jose import jwt, JWTError

#function for checking if auth header contains bearer , and extracting the token- auth header comes from routing file 
def extract_token(auth_header: str):
    #if header is missing or empty
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Missing authorization header"
        )
    
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authorization header format"
        )
    
    #splitting string and returning only token part 
    try:
        token = auth_header.split(" ", 1)[1]
        return token
    except IndexError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Token missing from the bearer"
        )
    

def verify_token(token:str):

    try:
        #decoding and then verifying the signature , internally comparing it also , if success return payload
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid or expired token"
        )
    return payload
