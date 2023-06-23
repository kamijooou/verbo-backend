import uuid
from typing import Optional

from pydantic import BaseModel


class ComixBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class ComixCreate(ComixBase):
    title: str


class ComixUpdate(ComixBase):
    pass


class ComixInDBBase(ComixBase):
    id: uuid.UUID
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class Comix(ComixInDBBase):
    pass
