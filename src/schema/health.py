from pydantic import Field

from src.common.basemodel import BaseModel


class GetHealthOut(BaseModel):
	status: str = Field(description="The status of the service.")
	message: str = Field(description="The message of the service.")
