import typing
from sqlalchemy.ext.asyncio import AsyncSession
from app.users import models, schema


async def get_user_by_email(db: AsyncSession, email: str) -> typing.Tuple[bool, typing.Union[models.User, None]]:
    db_user = await db.query(models.User).filter(models.User.email == email).first()
    if db_user:
        return True, db_user
    return False, None


async def create_user(db: AsyncSession, user: schema.SignupRequest) -> bool:
    data = user.dict()
    data['password'] = schema.argon_ph.hash(data['password'])
    db_user = models.User(**data)
    await db.add(db_user)
    db.commit()
    return True
