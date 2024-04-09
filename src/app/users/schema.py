import time
from datetime import datetime, timedelta
from uuid import UUID
from enum import Enum
from jose import jwt
from pydantic import BaseModel, constr, EmailStr
from fastapi import HTTPException
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from app import settings

argon_ph = PasswordHasher()


class SignupRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class TokenAccessTypeEnum(str, Enum):
    user = 'user'


class TokenTypeEnum(str, Enum):
    bearer = 'Bearer'


class TokenResponse(BaseModel):
    access_token: str
    token_type: TokenTypeEnum


class UserAuth(BaseModel):
    id: UUID
    password: str

    class Config:
        orm_mode = True

    def verify_password(
        self,
        plain_password: str,
        err_message: str = "Username or password does not match",
    ):
        try:
            argon_ph.verify(self.password, plain_password)
        except VerifyMismatchError:
            raise HTTPException(400, err_message)

    def generate_token(self):
        token = jwt.encode(
            {
                "exp": datetime.utcnow() + timedelta(days=1),
                "user_id": str(self.id),
                "access": TokenAccessTypeEnum.user,
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )
        return TokenResponse(access_token=token, token_type=TokenTypeEnum.bearer)