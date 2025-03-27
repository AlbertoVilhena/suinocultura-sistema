from fastapi import APIRouter

router = APIRouter(prefix="/lotes", tags=["Lotes"])

@router.get("/")
def listar_lotes():
    return []

@router.post("/")
def criar_lote():
    return {"msg": "Lote criado"}
