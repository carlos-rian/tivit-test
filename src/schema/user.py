from enum import Enum

from pydantic import EmailStr

from src.common.basemodel import BaseModel


# user
class GetUserPurchase(BaseModel):
	id: int
	item: str
	price: float


class GetUserData(BaseModel):
	name: str
	email: EmailStr
	purchases: list[GetUserPurchase]


class GetUserOut(BaseModel):
	message: str = "Hello, user!"
	data: GetUserData = GetUserData.model_validate(
		{
			"name": "John Doe",
			"email": "john@example.com",
			"purchases": [{"id": 1, "item": "Laptop", "price": 2500}, {"id": 2, "item": "Smartphone", "price": 1200}],
		}
	)


# admin


class EnumAdminStatus(str, Enum):
	COMPLETED = "Completed"
	PENDING = "Pending"


class GetAdminReport(BaseModel):
	id: int
	title: str
	status: EnumAdminStatus


class GetAdminData(BaseModel):
	name: str
	email: EmailStr
	reports: list[GetAdminReport]


class GetAdminOut(BaseModel):
	message: str = "Hello, admin!"
	data: GetAdminData = GetAdminData.model_validate(
		{
			"name": "Admin Master",
			"email": "admin@example.com",
			"reports": [
				{"id": 1, "title": "Monthly Sales", "status": "Completed"},
				{"id": 2, "title": "User Activity", "status": "Pending"},
			],
		}
	)
