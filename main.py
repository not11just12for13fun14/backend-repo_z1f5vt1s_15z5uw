import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from bson.objectid import ObjectId

from database import db, create_document, get_documents
from schemas import Riceproduct, Order

app = FastAPI(title="Rice Merchant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Rice Merchant Backend Running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Product Endpoints
@app.post("/api/products")
def create_product(product: Riceproduct):
    try:
        inserted_id = create_document("riceproduct", product)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/products")
def list_products():
    try:
        docs = get_documents("riceproduct")
        # Serialize ObjectId and timestamps
        for d in docs:
            d["id"] = str(d.get("_id"))
            d.pop("_id", None)
            if "created_at" in d:
                d["created_at"] = str(d["created_at"])  # simple string serialize
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"])  # simple string serialize
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Order Endpoints
@app.post("/api/orders")
def create_order(order: Order):
    try:
        # Basic stock check (optional): ensure items exist
        for item in order.items:
            try:
                # verify product exists
                pid = ObjectId(item.product_id)
                prod = db["riceproduct"].find_one({"_id": pid})
                if not prod:
                    raise HTTPException(status_code=404, detail=f"Product not found: {item.product_id}")
            except Exception:
                raise HTTPException(status_code=400, detail=f"Invalid product id: {item.product_id}")
        inserted_id = create_document("order", order)
        return {"id": inserted_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders")
def list_orders():
    try:
        docs = get_documents("order", limit=50)
        for d in docs:
            d["id"] = str(d.get("_id"))
            d.pop("_id", None)
            if "created_at" in d:
                d["created_at"] = str(d["created_at"])  # simple string serialize
            if "updated_at" in d:
                d["updated_at"] = str(d["updated_at"])  # simple string serialize
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
