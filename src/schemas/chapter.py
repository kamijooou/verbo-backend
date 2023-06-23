import uuid
from typing import Optional, List

from pydantic import BaseModel


class ChapterBase(BaseModel):
    title: Optional[str] = None
    pages: Optional[List[str]] = None


class ChapterCreate(ChapterBase):
    title: str


class ChapterUpdate(ChapterBase):
    title: str
    pages: Optional[List[str]]


class ChapterInDBBase(ChapterBase):
    id: uuid.UUID
    title: str
    comix_id: uuid.UUID

    class Config:
        orm_mode = True


class Chapter(ChapterInDBBase):
    pages: List[str]
