from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Defining the structure expected in JSON for endpoint
class UserUpdate(BaseModel):
    name: str

users_db = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Peter"},
]

@app.get("/users")
def get_users():
    return users_db

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_data: UserUpdate):

    for user in users_db:
        if user["id"] == user_id:
            user["name"] = updated_data.name
            return {"message": "User updated successfully", "user": user}

    raise HTTPException(status_code=404, detail="User not found")