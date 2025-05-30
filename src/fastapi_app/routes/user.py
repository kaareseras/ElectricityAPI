import pathlib

from fastapi import APIRouter, BackgroundTasks, Depends, Header, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.security import get_current_admin, get_current_user, oauth2_scheme
from src.fastapi_app.responses.user import LoginResponse, UserResponse
from src.fastapi_app.schemas.user import (
    EmailRequest,
    RegisterUserRequest,
    ResetRequest,
    UpdateUserRequest,
    VerifyUserRequest,
)
from src.fastapi_app.services import user

parent_path = pathlib.Path(__file__).parent.parent.parent
templates = Jinja2Templates(directory=parent_path / "templates")


user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

auth_router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme), Depends(get_current_user)],
)

guest_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)


@user_router.post("", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    data: RegisterUserRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_db_session),
):
    return await user.create_user_account(data, session, background_tasks)


@user_router.post("/update", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def update_user(
    data: UpdateUserRequest,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_db_session),
    current_user=Depends(get_current_user),
):
    return await user.update_user_account(data, session, background_tasks, current_user)


@user_router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_user_account(
    data: VerifyUserRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_db_session)
):
    await user.activate_user_account(data, session, background_tasks)
    return JSONResponse({"message": "Account is activated successfully."})


@guest_router.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def user_login(data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_db_session)):
    return await user.get_login_token(data, session)


@guest_router.post("/refresh", status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def refresh_token(refresh_token=Header(), session: Session = Depends(get_db_session)):
    return await user.get_refresh_token(refresh_token, session)


@guest_router.post("/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(
    data: EmailRequest, background_tasks: BackgroundTasks, session: Session = Depends(get_db_session)
):
    await user.email_forgot_password_link(data, background_tasks, session)
    return JSONResponse({"message": "A email with password reset link has been sent to you."})


@guest_router.put("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(data: ResetRequest, session: Session = Depends(get_db_session)):
    await user.reset_user_password(data, session)
    return JSONResponse({"message": "Your password has been updated."})


@auth_router.get("", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def fetch_users(session: Session = Depends(get_db_session), admin=Depends(get_current_admin)):
    return await user.fetch_all_users(session)


@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def fetch_user(user=Depends(get_current_user)):
    return user


@auth_router.get("/{pk}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_info(pk, session: Session = Depends(get_db_session)):
    return await user.fetch_user_detail(pk, session)


@auth_router.delete("/{pk}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def delete_user(
    pk: int,
    session: Session = Depends(get_db_session),
    current_user=Depends(get_current_admin),
):
    return await user.delete_user_account(pk, session, current_user)


@auth_router.put("/admin/{pk}/{is_admin}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user_admin(
    pk: int,
    is_admin: bool,
    session: Session = Depends(get_db_session),
    current_user=Depends(get_current_admin),
):
    return await user.update_user_admin(pk, is_admin, session, current_user)


@user_router.get("/detailspage", response_class=HTMLResponse, name="users_detailspage")
async def details(request: Request, session: Session = Depends(get_db_session)):
    return templates.TemplateResponse("user/Useraccountsettings.html", {"request": request})
