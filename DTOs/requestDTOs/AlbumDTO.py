from pydantic import BaseModel

class AlbumDTO(BaseModel):
    title: str
    artist: str
