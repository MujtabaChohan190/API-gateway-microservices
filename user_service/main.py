from fastapi import FastAPI
app = FastAPI()
@app.get("/users")
def getuser():
    return [
        {"id":1, "name": "Alice"},
        {"id":2, "name": "Peter"},
    ]
