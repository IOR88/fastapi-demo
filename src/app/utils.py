from typing import Union, Any, List
from sqlalchemy.ext.asyncio import AsyncSession


async def sql_create_data(session: AsyncSession, data: Union[Any, List[Any]]) -> Union[Any, List[Any]]:
    for item in data if isinstance(data, list) else [data]:
        try:
            session.add(item)
            await session.commit()
            await session.refresh(item)
        except Exception as e:
            await session.rollback()
            raise e
    return data
