from enum import Enum
from pydantic import BaseModel, constr, EmailStr


class SignupRequest(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class TokenTypeEnum(str, Enum):
    bearer = 'Bearer'


class TokenResponse(BaseModel):
    access_token: str
    token_type: TokenTypeEnum
