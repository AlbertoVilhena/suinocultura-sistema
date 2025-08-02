from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nome: str

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        orm_mode = True
