from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ProductUpdate(BaseModel):
    name: str

products_db = [
    {"id": 1, "name": "Laptop"},
    {"id": 2, "name": "Phone"},
]

@app.get("/products")
def getproducts():
    return products_db

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_data: ProductUpdate):

    for product in products_db:
        if product["id"] == product_id:
            product["name"] = updated_data.name
            return {"message": "Product updated successfully", "product": product}
            
    raise HTTPException(status_code=404, detail="Product not found")