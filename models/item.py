from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ItemOut(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    created_at: datetime
