from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.followers import models, schema
from app.utils import sql_create_data


async def add_relationship(db_session: AsyncSession, from_user: schema.User, to_user: schema.User) -> bool:
    await sql_create_data(db_session, models.Relationship(from_user=from_user.id, to_user=to_user.id))
    return True


async def delete_relationship(db_session: AsyncSession, from_user: schema.User, to_user: schema.User) -> bool:
    query = delete(models.Relationship).where(
        models.Relationship.from_user == from_user.id,
        models.Relationship.to_user == to_user.id, )
    await db_session.execute(query)
    await db_session.commit()
    return True


async def stats(db_session: AsyncSession, user: schema.User) -> schema.Stats:
    following = await db_session.scalar(func.count(models.Relationship.id).filter(models.Relationship.from_user == user.id))
    followers = await db_session.scalar(func.count(models.Relationship.id).filter(models.Relationship.to_user == user.id))
    return schema.Stats(following=following, followers=followers)
