from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from repository.ormBase import Base

class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    albums = relationship("Album", back_populates="artist")

