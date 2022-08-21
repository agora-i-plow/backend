from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.utils.get_settings import get_fastapi_settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    settings = get_fastapi_settings()
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.FASTAPI_HASH_EXPIRATION)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.FASTAPI_SECRET, algorithm=settings.FASTAPI_HASH_ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str, credentails_exception) -> str:
    settings = get_fastapi_settings()
    try:
        playload = jwt.decode(
            token, settings.FASTAPI_SECRET, algorithms=[settings.FASTAPI_HASH_ALGORITHM]
        )
        login: str = playload.get("sub")
        if login is None:
            raise credentails_exception
    except JWTError:
        raise credentails_exception from JWTError
    return login


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentails_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentails_exception)
