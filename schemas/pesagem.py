from pydantic import BaseModel
from datetime import date
from typing import Optional

class PesagemBase(BaseModel):
    lote_id: int
    peso_medio: float
    data_pesagem: date
    observacoes: Optional[str] = None

class PesagemCreate(PesagemBase):
    pass

class PesagemUpdate(PesagemBase):
    pass

class PesagemOut(PesagemBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
