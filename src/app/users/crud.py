import typing
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.users import models, schema
from app.utils import sql_create_data


async def get_user_by_user_id(db_session: AsyncSession, user_id: str) -> typing.Tuple[bool, typing.Union[models.User, None]]:
    db_user = (await db_session.scalars(select(models.User).where(models.User.id == user_id))).first()
    if db_user:
        return True, db_user
    return False, None


async def create_user(db_session: AsyncSession, user: schema.SignupRequest) -> bool:
    data = user.dict()
    data['password'] = schema.argon_ph.hash(data['password'])
    await sql_create_data(db_session, models.User(**data))
    return True
