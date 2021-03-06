from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy_utils import generic_repr

from app.db.session import Base


@generic_repr
class Location(Base):
    __tablename__ = "location"

    # columns
    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True, nullable=False)
    state = Column(String, index=True, nullable=False)
    country = Column(String, nullable=False)

    # relationships
    restaurants = relationship("Restaurant", back_populates="location")