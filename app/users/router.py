from fastapi import APIRouter

from app.users.schemas import UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("", response_model=list[UserRead])
async def get_users() -> list[UserRead]:
    return []
