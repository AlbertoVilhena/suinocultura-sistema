from fastapi import APIRouter

router = APIRouter(prefix="/ia", tags=["Inteligência Artificial"])

@router.get("/")
def obter_recomendacoes():
    return {"msg": "Recomendações de IA"}
