from typing import Annotated
from app import settings
from app.dependencies.dbsession import db_session_dep
from app.users.crud import get_user_by_user_id
from app.users import models
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError


def decode_token(token: str):
    return jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)


async def get_current_user(token: str, db_session: db_session_dep) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception
    ok, user = await get_user_by_user_id(db_session, user_id)
    if user is None or not ok:
        raise credentials_exception
    return user


current_user_dep = Annotated[models.User, Depends(get_current_user)]
