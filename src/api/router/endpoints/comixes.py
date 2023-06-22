import uuid
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src import crud, models, schemas
from src.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Comix])
def read_comixes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve comixes.
    """
    if crud.user.is_superuser(current_user):
        comixes = crud.comix.get_multi(db, skip=skip, limit=limit)
    else:
        comixes = crud.comix.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return comixes


@router.post("/", response_model=schemas.Comix)
def create_comix(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ComixCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new comix.
    """
    comix = crud.comix.create_with_owner(db=db, obj_in=item_in, owner_id=current_user.id)
    return comix


@router.put("/{id}", response_model=schemas.Comix)
def update_comix(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    item_in: schemas.ComixUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a comix.
    """
    comix = crud.comix.get(db=db, id=id)
    if not comix:
        raise HTTPException(status_code=404, detail="Comix not found")
    if not crud.user.is_superuser(current_user) and (comix.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    comix = crud.comix.update(db=db, db_obj=comix, obj_in=item_in)
    return comix


@router.get("/{id}", response_model=schemas.Comix)
def read_comix(
    *,
    db: Session = Depends(deps.get_db),
    id: uuid.UUID,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get comix by ID.
    """
    comix = crud.comix.get(db=db, id=id)
    if not comix:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (comix.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return comix


@router.delete("/{id}", response_model=schemas.Comix)
def delete_comix(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a comix.
    """
    comix = crud.comix.get(db=db, id=id)
    if not comix:
        raise HTTPException(status_code=404, detail="Item not found")
    if not crud.user.is_superuser(current_user) and (comix.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    comix = crud.comix.remove(db=db, id=id)
    return comix