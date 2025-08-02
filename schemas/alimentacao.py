from pydantic import BaseModel
from datetime import date
from typing import Optional

class AlimentacaoBase(BaseModel):
    lote_id: int
    tipo_racao: str
    quantidade_kg: float
    data_fornecida: date
    observacoes: Optional[str] = None

class AlimentacaoCreate(AlimentacaoBase):
    pass

class AlimentacaoUpdate(AlimentacaoBase):
    pass

class AlimentacaoOut(AlimentacaoBase):
    id: int

    class Config:
        from_attributes = True
