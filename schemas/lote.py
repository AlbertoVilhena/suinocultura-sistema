from pydantic import BaseModel
from datetime import date

class LoteBase(BaseModel):
    nome: str
    data_inicio: date
    tipo_racao: str

class LoteCreate(LoteBase):
    pass

class LoteUpdate(LoteBase):
    pass

class LoteOut(LoteBase):
    id: int

    class Config:
        orm_mode = True
