import logging

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/result",
    tags=["result"],
    responses={
        200: {"description": "Get successful"}
    },
)


@router.get("/page/{id}")
async def render_result_page(request: Request, id: int):
    return templates.TemplateResponse("result.html", {"request": request, "id": id})


@router.get("/{id}")
async def get_result(id: int):
    pass