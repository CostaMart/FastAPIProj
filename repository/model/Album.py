from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship
from repository.ormBase import Base

class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    artist_id = Column(Integer, ForeignKey("artist.id"))
    artist = relationship("Artist", back_populates="albums")



