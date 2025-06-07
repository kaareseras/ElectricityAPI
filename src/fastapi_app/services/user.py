import logging
from datetime import UTC, datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.config.security import (
    generate_token,
    get_token_payload,
    hash_password,
    is_password_strong_enough,
    load_user,
    str_decode,
    str_encode,
    verify_password,
)
from src.fastapi_app.models.user import User, UserToken
from src.fastapi_app.services.email import (
    send_account_activation_confirmation_email,
    send_account_verification_email,
    send_password_reset_email,
)
from src.fastapi_app.utils.email_context import FORGOT_PASSWORD, USER_VERIFY_ACCOUNT
from src.fastapi_app.utils.string import unique_string

settings = get_settings()


async def create_user_account(data, session, background_tasks):
    user_exist = session.query(User).filter(func.lower(User.email) == func.lower(data.email)).first()
    if user_exist:
        raise HTTPException(status_code=400, detail="Email already exists.")

    if not is_password_strong_enough(data.password):
        raise HTTPException(status_code=400, detail="Please provide a strong password.")

    user = User()
    user.name = data.name
    user.email = data.email
    user.password = hash_password(data.password)
    user.is_active = False
    user.updated_at = datetime.now(UTC)
    session.add(user)
    session.commit()
    session.refresh(user)

    # Account Verification Email
    await send_account_verification_email(user, background_tasks=background_tasks)
    return user


async def update_user_account(data, session, background_tasks, current_user):
    user = session.query(User).filter(User.id == current_user.id).first()

    # Check if email has changed, if changed, invalidate current user and send verification email
    if user.email != data.email:
        await send_account_verification_email(user, background_tasks=background_tasks)
        user.verified_at = None
        user.is_active = False

    user.name = data.name
    user.email = data.email
    user.updated_at = datetime.now(UTC)
    session.commit()
    session.refresh(user)

    return user


async def activate_user_account(data, session, background_tasks):
    user = session.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="This link is not valid.")

    user_token = user.get_context_string(context=USER_VERIFY_ACCOUNT)
    try:
        token_valid = verify_password(user_token, data.token)
    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False
    if not token_valid:
        raise HTTPException(status_code=400, detail="This link either expired or not valid.")

    user.is_active = True
    user.updated_at = datetime.now(UTC)
    user.verified_at = datetime.now(UTC)
    session.add(user)
    session.commit()
    session.refresh(user)
    # Activation confirmation email
    await send_account_activation_confirmation_email(user, background_tasks)
    return user


async def get_login_token(data, session):
    # verify the email and password
    # Verify that user account is verified
    # Verify user account is active
    # generate access_token and refresh_token and ttl

    user = await load_user(data.username, session)
    if not user:
        raise HTTPException(status_code=400, detail="Email is not registered with us.")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password.")

    if not user.verified_at:
        raise HTTPException(
            status_code=400,
            detail="Your account is not verified. Please check your email inbox to verify your account.",
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account has been dactivated. Please contact support.")

    # Generate the JWT Token
    return _generate_tokens(user, session)


async def get_refresh_token(refresh_token, session):
    token_payload = get_token_payload(refresh_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
    if not token_payload:
        raise HTTPException(status_code=400, detail="Invalid Request.")

    refresh_key = token_payload.get("t")
    access_key = token_payload.get("a")
    user_id = str_decode(token_payload.get("sub"))
    user_token = (
        session.query(UserToken)
        .options(joinedload(UserToken.user))
        .filter(
            UserToken.refresh_key == refresh_key,
            UserToken.access_key == access_key,
            UserToken.user_id == user_id,
            UserToken.expires_at > datetime.now(UTC),
        )
        .first()
    )
    if not user_token:
        raise HTTPException(status_code=400, detail="Invalid Request.")

    user_token.expires_at = datetime.now(UTC)
    session.add(user_token)
    session.commit()
    return _generate_tokens(user_token.user, session)


def _generate_tokens(user, session):
    refresh_key = unique_string(100)
    access_key = unique_string(50)
    rt_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    user_token = UserToken()
    user_token.user_id = user.id
    user_token.refresh_key = refresh_key
    user_token.access_key = access_key
    user_token.expires_at = datetime.now(UTC) + rt_expires
    session.add(user_token)
    session.commit()
    session.refresh(user_token)

    at_payload = {
        "sub": str_encode(str(user.id)),
        "a": access_key,
        "r": str_encode(str(user_token.id)),
        "n": str_encode(f"{user.name}"),
    }

    at_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = generate_token(at_payload, settings.JWT_SECRET, settings.JWT_ALGORITHM, at_expires)

    rt_payload = {"sub": str_encode(str(user.id)), "t": refresh_key, "a": access_key}
    refresh_token = generate_token(rt_payload, settings.SECRET_KEY, settings.JWT_ALGORITHM, rt_expires)
    return {"access_token": access_token, "refresh_token": refresh_token, "expires_in": at_expires.seconds}


async def email_forgot_password_link(data, background_tasks, session):
    user = await load_user(data.email, session)
    if not user:
        return
    if not user.verified_at:
        raise HTTPException(
            status_code=400,
            detail="Your account is not verified. Please check your email inbox to verify your account.",
        )

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Your account has been dactivated. Please contact support.")

    await send_password_reset_email(user, background_tasks)


async def reset_user_password(data, session):
    user = await load_user(data.email, session)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid request")

    if not user.verified_at:
        raise HTTPException(status_code=400, detail="Invalid request")

    if not user.is_active:
        raise HTTPException(status_code=400, detail="Invalid request")

    user_token = user.get_context_string(context=FORGOT_PASSWORD)
    try:
        token_valid = verify_password(user_token, data.token)
    except Exception as verify_exec:
        logging.exception(verify_exec)
        token_valid = False
    if not token_valid:
        raise HTTPException(status_code=400, detail="Invalid window.")

    user.password = hash_password(data.password)
    user.updated_at = datetime.now(UTC)
    session.add(user)
    session.commit()
    session.refresh(user)
    # Notify user that password has been updated


async def fetch_user_detail(pk, session):
    user = session.query(User).filter(User.id == pk).first()
    if user:
        return user
    raise HTTPException(status_code=400, detail="User does not exists.")


async def delete_user_account(pk, session, current_user):
    user = session.query(User).filter(User.id == pk).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if current_user.id == pk:
        raise HTTPException(status_code=400, detail="You cannot delete your own account.")

    session.delete(user)
    session.commit()
    return user


async def update_user_admin(pk, is_admin, session, current_user):
    user = session.query(User).filter(User.id == pk).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    if current_user.id == pk:
        raise HTTPException(status_code=400, detail="You cannot update your own account.")

    user.is_admin = is_admin
    session.commit()
    return user


async def fetch_all_users(session):
    users = session.query(User).order_by(User.email.asc()).all()
    if not users:
        raise HTTPException(status_code=400, detail="No users found.")

    user_responses = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "is_active": user.is_active,
            "is_admin": user.is_admin,
            "created_at": user.created_at,
        }
        for user in users
    ]
    return user_responses
