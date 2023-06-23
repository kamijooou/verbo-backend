from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, UUID, String, ARRAY, text
from sqlalchemy.orm import relationship

from src.db.base_class import Base

if TYPE_CHECKING:
    from .comix import Comix  # noqa: F401


class Chapter(Base):
    id = Column(UUID, primary_key=True, default=text("uuid_generate_v4()"), index=True)
    title = Column(String, index=True, nullable=False)
    pages = Column(ARRAY(String), default=[])
    comix_id = Column(UUID, ForeignKey("comix.id"))
    comix = relationship("Comix", back_populates="chapters")
