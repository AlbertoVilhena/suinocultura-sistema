from fastapi import APIRouter

router = APIRouter(prefix="/estoque", tags=["Estoque"])

@router.get("/")
def listar_estoque():
    return []

@router.post("/")
def atualizar_estoque():
    return {"msg": "Estoque atualizado"}
