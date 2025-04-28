import pathlib

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.fastapi_app.config.security import get_current_admin, oauth2_scheme

parent_path = pathlib.Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=parent_path / "templates")


admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_admin)],
)


@admin_router.get("", response_class=HTMLResponse, name="admin_index")
async def details(request: Request):
    return templates.TemplateResponse("user/Useraccountsettings.html", {"request": request})
