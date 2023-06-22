from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, UUID, String, text
from sqlalchemy.orm import relationship

from src.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class Comix(Base):
    id = Column(UUID, primary_key=True, default=text("uuid_generate_v4()"), index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(UUID, ForeignKey("user.id"))
    owner = relationship("User", back_populates="comixes")
