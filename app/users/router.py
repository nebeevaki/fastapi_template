from fastapi import APIRouter

from app.db.session import SessionDep
from app.users.models import User
from app.users.schemas import UserRead
from app.users.service import list_users

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=list[UserRead])
async def get_users(session: SessionDep) -> list[User]:
    return await list_users(session)
