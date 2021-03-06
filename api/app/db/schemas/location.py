from pydantic import BaseModel


class LocationBase(BaseModel):
    city: str
    state: str
    country: str


class LocationItem(LocationBase):
    class Config:
        orm_mode = True
