# =========================
# main.py - Euron API 🚀
# =========================
"""
Euron API - FastAPI + MongoDB
-----------------------------
This FastAPI application connects to MongoDB to store, update, and retrieve
user/course data. Endpoints included:

- GET /           → Health check
- GET /get_eurondata → Fetch all records
- POST /euron/insert_data → Insert new record
- PUT /euron/update_data/{id} → Full update
- PATCH /euron/patch_data/{id} → Partial update
- DELETE /euron/delete_data/{id} → Delete record

Legend for endpoint numbering:
------------------------------
7a — GET /            ✅ Health check
7b — GET /get_eurondata 📋 Read all
7c — POST /euron/insert_data ➕ Create
7d — PUT /euron/update_data/{id} ✏️ Full update
7e — PATCH /euron/patch_data/{id} 🖊️ Partial update
7f — DELETE /euron/delete_data/{id} ❌ Delete
"""

# =========================
# 1️⃣ IMPORTS 📦
# =========================
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

# =========================
# 2️⃣ ENVIRONMENT VARIABLES 🌱
# =========================
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "eurondb")

if not MONGO_URI:
    raise RuntimeError("MONGODB_URI is not set")  # Stop execution if MongoDB URI missing

# =========================
# 3️⃣ MONGODB CLIENT SETUP 🗄️
# =========================
client = AsyncIOMotorClient(MONGO_URI)  # Connect to MongoDB
db = client[DB_NAME]                     # Access the database
euron_data = db["euron_coll"]           # Access the collection

# =========================
# 4️⃣ FASTAPI APP INITIALIZATION ⚡
# =========================
app = FastAPI(
    title="Euron API",
    version="1.1",
    description="API to store, update, and retrieve user/course data with MongoDB"
)

# =========================
# 5️⃣ PYDANTIC MODELS 📝
# =========================
class EuronData(BaseModel):
    name: str
    phone: int
    city: str
    course: str

class PartialEuronData(BaseModel):
    name: str | None = None
    phone: int | None = None
    city: str | None = None
    course: str | None = None

# =========================
# 6️⃣ HELPER FUNCTIONS 🛠️
# =========================
def serialize_mongo(doc: dict) -> dict:
    """
    Converts MongoDB document to JSON-friendly format:
    - Converts _id (ObjectId) to string
    - Renames _id to 'id'
    """
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc

# =========================
# 7️⃣ API ENDPOINTS 🌐
# =========================
"""
MongoDB & API Workflow Overview:

          Client
            |
     ----------------
     | POST / GET   |
     ----------------
            |
          FastAPI
            |
   --------------------
   | Endpoint Logic   |
   | (Insert / Find)  |
   --------------------
            |
        MongoDB
      (euron_coll)
            |
      ----------------
      | Response JSON |
      ----------------
"""

# -------------------------
# 7a — GET / ✅ Health check
# -------------------------
@app.get("/")
async def root():
    return {"status": "success", "message": "API is running"}

# -------------------------
# 7b — GET /get_eurondata 📋 Read all
# -------------------------
@app.get("/get_eurondata")
async def get_all_data():
    try:
        documents = []
        async for doc in euron_data.find():
            documents.append(serialize_mongo(doc))
        return {"status": "success", "count": len(documents), "data": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# 7c — POST /euron/insert_data ➕ Create
# -------------------------
@app.post("/euron/insert_data")
async def insert_euron_data(data: EuronData):
    try:
        result = await euron_data.insert_one(data.model_dump())
        ObjectIdStr = str(result.inserted_id)
        return {
            "status": "success",
            "message": "Record inserted successfully",
            "id": ObjectIdStr
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# 7d — PUT /euron/update_data/{id} ✏️ Full update
# -------------------------
@app.put("/euron/update_data/{id}")
async def full_update_data(id: str, data: EuronData):
    try:
        result = await euron_data.replace_one({"_id": ObjectId(id)}, data.model_dump())
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Record with id {id} not found")
        return {
            "status": "success",
            "message": f"Record with id {id} fully updated"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# 7e — PATCH /euron/patch_data/{id} 🖊️ Partial update
# -------------------------
@app.patch("/euron/patch_data/{id}")
async def partial_update_data(id: str, data: PartialEuronData):
    try:
        update_data = {k: v for k, v in data.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        result = await euron_data.update_one({"_id": ObjectId(id)}, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Record with id {id} not found")
        return {
            "status": "success",
            "message": f"Record with id {id} partially updated ({len(update_data)} fields)"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------
# 7f — DELETE /euron/delete_data/{id} ❌ Delete
# -------------------------
@app.delete("/euron/delete_data/{id}")
async def delete_data(id: str):
    try:
        result = await euron_data.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"Record with id {id} not found")
        return {
            "status": "success",
            "message": f"Record with id {id} deleted successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# =========================
# 8️⃣ RUN THE APP 🚀
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
