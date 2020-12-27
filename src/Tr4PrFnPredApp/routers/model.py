import logging

from fastapi import APIRouter


router = APIRouter(
    prefix="/model",
    tags=["model"],
    responses={
        200: {"description": "Get successful"}
    },
)


@router.get("/")
async def get_models():
    pass


@router.get("/:id")
async def get_model(id: int):
    pass
