from fastapi import APIRouter, HTTPException
from app.dependencies.dbsession import db_session_dep
from app.dependencies.user import get_current_user
from app.followers import schema, crud
from app.schema import BasicMessage

router = APIRouter(
    prefix="/v1/followers",
    tags=["followers"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/me",
    response_model=None,
    dependencies=None,
)
async def me(
    db_session: db_session_dep,
):
    return None


@router.post("/follow", response_model=BasicMessage)
async def follow(db_session: db_session_dep,
                 current_user: get_current_user,
                 data: schema.User):
    try:
        await crud.add_relationship(db_session, from_user=schema.User(id=current_user.id), to_user=data)
        return BasicMessage(detail="Success")
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/unfollow", response_model=BasicMessage)
async def unfollow(db_session: db_session_dep,
                   current_user: get_current_user,
                   data: schema.User):
    try:
        await crud.delete_relationship(db_session, from_user=schema.User(id=current_user.id), to_user=data)
        return BasicMessage(detail="Success")
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/stats", response_model=schema.Stats)
async def stats(
        db_session: db_session_dep,
        current_user: get_current_user
):
    return await crud.stats(db_session, user=schema.User(id=current_user.id))
