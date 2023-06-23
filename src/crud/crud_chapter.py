import uuid
from typing import List, Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.crud.base import CRUDBase
from src.models.chapter import Chapter
from src.schemas.chapter import ChapterCreate, ChapterUpdate


class CRUDComix(CRUDBase[Chapter, ChapterCreate, ChapterUpdate]):
    def create_with_comix(
        self, db: Session, *, obj_in: ChapterCreate, comix_id: uuid.UUID
    ) -> Chapter:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, comix_id=comix_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_comix(
        self, db: Session, *, comix_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Chapter]:
        return (
            db.query(self.model)
            .filter(Chapter.comix_id == comix_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    # TODO: optimize pages changing
    def update(
        self, db: Session, *, db_obj: Chapter, obj_in: ChapterUpdate
    ) -> Chapter:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

chapter = CRUDComix(Chapter)
