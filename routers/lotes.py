from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.utils.auth import verificar_token

router = APIRouter()
lotes_data = []

class Lote(BaseModel):
    nome: str

@router.get("/lotes")
def listar_lotes(email: str = Depends(verificar_token)):
    return lotes_data

@router.post("/lotes")
def adicionar_lote(lote: Lote, email: str = Depends(verificar_token)):
    lotes_data.append({ "nome": lote.nome, "usuario": email })
    return {"mensagem": "Lote adicionado com sucesso"}
