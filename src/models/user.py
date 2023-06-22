from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, UUID, String, text
from sqlalchemy.orm import relationship

from src.db.base_class import Base

if TYPE_CHECKING:
    from .comix import Comix  # noqa: F401


class User(Base):
    id = Column(UUID, primary_key=True, default=text("uuid_generate_v4()"), index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    comixes = relationship("Comix", back_populates="owner")
