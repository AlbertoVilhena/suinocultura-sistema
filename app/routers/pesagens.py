from fastapi import APIRouter

router = APIRouter(prefix="/pesagens", tags=["Pesagens"])

@router.get("/")
def listar_pesagens():
    return []

@router.post("/")
def registrar_pesagem():
    return {"msg": "Pesagem registrada"}
