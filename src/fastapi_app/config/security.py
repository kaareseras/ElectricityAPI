import base64
import logging
from datetime import UTC, datetime, timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.fastapi_app.config.config import get_settings
from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.models.user import User, UserToken

SPECIAL_CHARACTERS = ["@", "#", "$", "%", "=", ":", "?", ".", "/", "|", "~", ">", "!"]

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False

    return True


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode("ascii")).decode("ascii")


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode("ascii")).decode("ascii")


def get_token_payload(token: str, secret: str, algo: str):
    try:
        payload = jwt.decode(token, secret, algorithms=algo)
    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {str(jwt_exec)}")
        payload = None
    return payload


def generate_token(payload: dict, secret: str, algo: str, expiry: timedelta):
    expire = datetime.now(UTC) + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, secret, algorithm=algo)


async def get_token_user(token: str, db):
    payload = get_token_payload(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    if payload:
        user_token_id = str_decode(payload.get("r"))
        user_id = str_decode(payload.get("sub"))
        access_key = payload.get("a")
        user_token = (
            db.query(UserToken)
            .options(joinedload(UserToken.user))
            .filter(
                UserToken.access_key == access_key,
                UserToken.id == user_token_id,
                UserToken.user_id == user_id,
                UserToken.expires_at > datetime.now(UTC),
            )
            .first()
        )
        if user_token:
            return user_token.user
    return None


async def load_user(email: str, db):
    try:
        user = db.query(User).filter(func.lower(User.email) == email.lower()).first()
    except Exception:
        logging.info(f"User Not Found, Email: {email}")
        user = None
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    user = await get_token_user(token=token, db=db)
    if user:
        return user
    raise HTTPException(status_code=401, detail="Not authorised.")


async def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    user = await get_token_user(token=token, db=db)
    if user.is_admin is True:
        return user
    raise HTTPException(status_code=403, detail="Admin access required.")
