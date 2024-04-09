from fastapi import APIRouter, HTTPException
from app.dependencies.dbsession import db_session_dep
from app.users import schema, crud
from app.schema import BasicMessage

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


@router.post("/signup", response_model=BasicMessage)
async def signup(db_session: db_session_dep,
                 data: schema.SignupRequest):
    try:
        await crud.create_user(db_session, data)
        return BasicMessage(detail="Sign-up success")
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/signin", response_model=schema.TokenResponse)
async def signin(db_session: db_session_dep,
                 data: schema.SignupRequest):
    obj = crud.get_user_by_email(db_session, data.email)
    if obj:
        user = schema.UserAuth.from_orm(obj)
        user.verify_password(data.password)
        return user.generate_token()

    raise HTTPException(400, "Username or password does not match")
