from fastapi import APIRouter, Depends
from .models import UserCreate, UserResponse, InfoMessage
from madokami.drivers.deps import SessionDep
from madokami.models import User
from madokami.crud import create_user, get_all_users, get_oauth2_client, add_oauth2_client
from madokami.drivers.deps import SessionDep, get_client_id

register_router = APIRouter(tags=["User"])


@register_router.post("/user/create", response_model=InfoMessage, dependencies=[Depends(get_client_id)])
def _create_user(*, user_in: UserCreate, session: SessionDep):
    new_user = User(username=user_in.username, password=user_in.password)
    try:
        create_user(session=session, user=new_user)
        return InfoMessage(message="User created successfully")
    except Exception as e:
        return InfoMessage(message=f"Failed to create user: {e}", success=False)


@register_router.get("/user/all", response_model=list[UserResponse])
def _get_users(session: SessionDep):
    users = [UserResponse(username=user.username, is_superuser=user.is_superuser) for user in get_all_users(session=session)]
    return users


@register_router.post("/user/login", response_model=InfoMessage)
def _user_login(session: SessionDep, user: UserCreate):
    try:
        token = add_oauth2_client(session=session, username=user.username, password=user.password)
        return InfoMessage(message="Login successful", data=token)
    except Exception as e:
        return InfoMessage(message=f"Login failed: {e}", success=False)

