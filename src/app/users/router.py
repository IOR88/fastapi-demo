from fastapi import APIRouter, Depends
from app.dependencies.dbsession import db_session_dep

router = APIRouter(
    prefix="/v1/users",
    tags=["users"],
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
