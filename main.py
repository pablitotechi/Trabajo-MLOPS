from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de datos
class Item(BaseModel):
    name: str
    description: str
    price: float
    in_stock: bool

# Base de datos simulada
items_db = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Store API!"}

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    items_db.append(item)
    return item

@app.get("/items/", response_model=List[Item])
def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id >= len(items_db) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    if item_id >= len(items_db) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id >= len(items_db) or item_id < 0:
        raise HTTPException(status_code=404, detail="Item not found")
    deleted_item = items_db.pop(item_id)
    return {"message": "Item deleted successfully", "item": deleted_item}
