import pathlib

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

parent_path = pathlib.Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=parent_path / "templates")


admin_router = APIRouter(prefix="/admin", tags=["Admin"], responses={404: {"description": "Not found"}})


@admin_router.get("", response_class=HTMLResponse, name="admin_index")
async def details(request: Request):
    return templates.TemplateResponse("admin/adminindex.html", {"request": request})
