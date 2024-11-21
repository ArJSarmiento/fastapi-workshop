from datetime import datetime
from fastapi import FastAPI
from models.constants import Message
from models.item import Item, ItemOut
from fastapi import Query, Path
from http import HTTPStatus

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(
    "/items/{item_id}",
    response_model=ItemOut,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    responses={
        HTTPStatus.NOT_FOUND: {"model": Message, "description": "Item not found"},
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": Message, "description": "Internal Server Error"},
    },
    summary="Get Item",
    description="Get item details for a product",
)
async def read_item(
    item_id: int = Path(..., description="The ID of the item to get"),
    q: str = Query(..., description="Query string"),
):
    print(item_id, q)
    return ItemOut(
        name=str(item_id),
        price=100,
        description=q,
        created_at=datetime.now(),
    )


@app.post(
    "/items",
    response_model=ItemOut,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    responses={
        HTTPStatus.INTERNAL_SERVER_ERROR: {"model": Message, "description": "Internal Server Error"},
    },
    summary="Create Item",
    description="Create item details for a product",
)
async def create_item(
    item: Item,
):
    response = ItemOut(
        **item.model_dump(),
        created_at=datetime.now(),
    )
    return response
