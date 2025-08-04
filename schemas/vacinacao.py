from pydantic import BaseModel
from datetime import date
from typing import Optional

class VacinacaoBase(BaseModel):
    lote_id: int
    vacina_nome: str
    data_aplicacao: date
    responsavel: str
    observacoes: Optional[str] = None

class VacinacaoCreate(VacinacaoBase):
    pass

class VacinacaoUpdate(VacinacaoBase):
    pass

class VacinacaoOut(VacinacaoBase):
    id: int

    class Config:
        from_attributes = True  # para Pydantic v2
