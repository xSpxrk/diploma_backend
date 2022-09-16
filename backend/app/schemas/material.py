from pydantic import BaseModel


class MaterialBase(BaseModel):
    material_id: int
    name: str


class Material(MaterialBase):
    class Config:
        orm_mode = True
