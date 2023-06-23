import uuid
from typing import Any, List

from starlette import status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Chapter])
def read_chapters(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
    comix_id: uuid.UUID | None = None
) -> Any:
    """
    Retrieve chapters from comix.
    """
    if not comix_id:
        raise HTTPException(status_code=404, detail="There is no chapter owner")
    if not (crud.user.is_superuser(current_user)\
    or (crud.comix.get(db=db, id=comix_id).owner_id == current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    chapters = crud.chapter.get_multi_by_comix(
        db, comix_id=comix_id, skip=skip, limit=limit
    )
    return chapters


@router.post("/", response_model=schemas.Chapter)
def create_chapter(
    *,
    db: Session = Depends(deps.get_db),
    chapter_in: schemas.ChapterCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
    comix_id: uuid.UUID | None = None
) -> Any:
    """
    Create new chapter for comix.
    """
    if not comix_id:
        raise HTTPException(status_code=400, detail="There is no chapter owner")
    if not (crud.user.is_superuser(current_user)\
    or (crud.comix.get(db=db, id=comix_id).owner_id == current_user.id)):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    chapter = crud.chapter.create_with_comix(
        db=db, obj_in=chapter_in, comix_id=comix_id
    )
    return chapter


# TODO: optimize image sending
@router.put("/{id}", response_model=schemas.Chapter)
def update_chapter(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    chapter_in: schemas.ChapterUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a chapter or images into it.
    """
    chapter = crud.chapter.get(db=db, id=id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    if not crud.user.is_superuser(current_user) and (chapter.comix.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    chapter = crud.comix.update(db=db, db_obj=chapter, obj_in=chapter_in)
    return chapter


@router.put("/{id}/clean")
def clean_page(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    
):
    pass


@router.get("/{id}", response_model=schemas.Chapter)
def read_chapter(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get chapter by ID.
    """
    chapter = crud.chapter.get(db=db, id=id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    if not crud.user.is_superuser(current_user) and (chapter.comix.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return chapter


@router.delete("/{id}", response_model=schemas.Chapter)
def delete_chapter(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a chapter from a comix.
    """
    chapter = crud.chapter.get(db=db, id=id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    if not crud.user.is_superuser(current_user) and (chapter.comix.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    chapter = crud.chapter.remove(db=db, id=id)
    return chapter