from fastapi import APIRouter, Depends

from src.common.basemodel import User, UserRole
from src.common.depedencies import Authentication
from src.schema.user import GetAdminOut, GetUserOut

router = APIRouter()


@router.get("/user", response_model=GetUserOut)
async def get_user(user: User = Depends(Authentication(UserRole.USER).authorization)):
	return GetUserOut()


@router.get("/admin", response_model=GetAdminOut)
async def get_admin(user: User = Depends(Authentication(UserRole.ADMIN).authorization)):
	return GetAdminOut()
