import enum
from decimal import Decimal

import humps
from pydantic import AliasChoices, AliasGenerator
from pysqlx_engine import BaseRow


def alias_resolve(field: str) -> AliasChoices:
	"""
	Resolve the alias for the field, to accept camelCase, PascalCase and snake_case

	:param field: The field name

	:return: The alias for the field

	"""
	return AliasChoices(field, humps.camelize(field), humps.pascalize(field))


def serialization_field(field: str) -> str:
	"""
	Convert the field to camelCase

	:param field: The field name
	:return: The field in camelCase

	"""
	return humps.camelize(field)


class BaseModel(BaseRow):
	model_config = {
		"populate_by_name": True,
		"from_attributes": True,
		"arbitrary_types_allowed": True,
		"alias_generator": AliasGenerator(alias=serialization_field, validation_alias=alias_resolve),
		"json_encoders": {
			Decimal: lambda v: str(v),
			ValueError: lambda v: str(v),
			bytes: lambda v: v.hex(),
		},
	}


class UserRole(enum.Enum):
	USER = "user"
	ADMIN = "admin"


class User(BaseModel):
	username: str
	role: UserRole
