from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

@app.post("/items/")
async def create_item(item: Item):
    return item
