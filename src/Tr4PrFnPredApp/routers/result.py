import logging

from fastapi import APIRouter


router = APIRouter(
    prefix="/reuslt",
    tags=["result"],
    responses={
        200: {"description": "Get successful"}
    },
)


@router.get("/:id")
async def get_result(id: int):
    pass