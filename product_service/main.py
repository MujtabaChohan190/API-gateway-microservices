from fastapi import FastAPI
app = FastAPI()

@app.get("/products")
def getproducts():
    return [
        {"id": 1 , "name" : "Laptop"},
        {"id" : 2 , "name" : "Phone"},
    ]

#for cath all
@app.delete("/products/{product_id}/reviews/{review_id}")
def delete_review(product_id : int , review_id : int):
    return {
        "message" : f"Successfully deleted review {review_id} for product {product_id}"
    }