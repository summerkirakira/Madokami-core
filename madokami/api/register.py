from fastapi import APIRouter, HTTPException
from .models import UserCreate, UserResponse
from madokami.drivers.deps import SessionDep
from madokami.models import User
from madokami.crud import create_user, get_all_users

register_router = APIRouter()


@register_router.post("/user/create", response_model=UserCreate)
def create_user(*, user_in: UserCreate, session: SessionDep):
    new_user = User(username=user_in.username, password=user_in.password)
    create_user(session=session, user=new_user)
    return new_user


@register_router.get("/user/all", response_model=list[UserResponse])
def get_all_users(session: SessionDep):
    users = [UserResponse(username=user.username, is_superuser=user.is_superuser) for user in get_all_users(session=session)]
    return users
