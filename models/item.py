from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ItemOut(Item):
    created_at: datetime
