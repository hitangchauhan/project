 from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGO_URL = os.getenv("MONGO_URL")

client = MongoClient(MONGO_URL)
db = client["shopdb"]
products_collection = db["products"]

@app.get("/")
def home():
    return {"message": "FastAPI backend is running 🚀"}

@app.get("/api/products")
def get_products():
    products = []
    for p in products_collection.find():
        products.append({
            "name": p["name"],
            "price": p["price"],
            "image": p.get("image", "")
        })
    return products

@app.post("/api/products")
def add_product(product: dict):
    products_collection.insert_one(product)
    return {"status": "Product added successfully"}
