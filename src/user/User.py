from pydantic import BaseModel, ConfigDict
from uuid import UUID


class UserIn(BaseModel):
    email: str
    password: str


class User(UserIn):
    id: UUID
    model_config = ConfigDict(from_attributes=True, extra="ignore")