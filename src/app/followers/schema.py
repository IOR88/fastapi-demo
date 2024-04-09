from uuid import UUID
from pydantic import BaseModel


class User(BaseModel):
    id: UUID


class Stats(BaseModel):
    followers_count: int
    following_count: int
