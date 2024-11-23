from datetime import datetime
from fastapi import FastAPI, Depends, Query, Path
from models.constants import Message
from models.item import Item, ItemOut
from http import HTTPStatus
from typing import List, Annotated
from auth import app as auth_app, User, get_current_active_user

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


async def common_parameters(
    q: str | None = Query(..., description="Query string"),
    item_id: int = Path(..., description="The ID of the item to get"),
):
    return {"q": q, "item_id": item_id}


@app.get(
    "/items/{item_id}",
    response_model=ItemOut,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    responses={
        HTTPStatus.NOT_FOUND: {"model": Message, "description": "Item not found"},
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            "model": Message,
            "description": "Internal Server Error",
        },
    },
    summary="Get Item",
    description="Get item details for a product",
)
async def read_item(params: dict = Depends(common_parameters)):
    print(params)
    return ItemOut(
        name=str(params["item_id"]),
        price=100,
        description=params["q"],
        created_at=datetime.now(),
    )


@app.get(
    "/items_list/{item_id}",
    dependencies=[Depends(common_parameters)],
    response_model=List[ItemOut],
)
async def read_item_list(params: dict = Depends(common_parameters)):
    return [
        ItemOut(
            name=str(params["item_id"]),
            price=100,
            description=params["q"],
            created_at=datetime.now(),
        )
    ]


@app.post(
    "/items",
    response_model=ItemOut,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    responses={
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            "model": Message,
            "description": "Internal Server Error",
        },
    },
    summary="Create Item",
    description="Create item details for a product",
)
async def create_item(
    item: Item,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    _ = current_user
    response = ItemOut(
        **item.model_dump(),
        created_at=datetime.now(),
    )
    return response


app.include_router(auth_app)
