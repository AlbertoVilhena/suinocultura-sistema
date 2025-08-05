from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.deps import get_db
from utils.auth import get_current_user  # ✅ substitui usuario_logado
from models.lote import Lote
from schemas import lote as schemas

router = APIRouter()

@router.post("/lotes", response_model=schemas.LoteOut)
def criar_lote(
    lote: schemas.LoteCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)  # ✅ autenticação via token
):
    novo = Lote(**lote.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

@router.get("/lotes", response_model=list[schemas.LoteOut])
def listar_lotes(
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    return db.query(Lote).all()

@router.get("/lotes/{lote_id}", response_model=schemas.LoteOut)
def buscar_lote(
    lote_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    lote = db.query(Lote).filter(Lote.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    return lote

@router.put("/lotes/{lote_id}", response_model=schemas.LoteOut)
def atualizar_lote(
    lote_id: int,
    dados: schemas.LoteUpdate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    lote = db.query(Lote).filter(Lote.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")

    for key, value in dados.dict().items():
        setattr(lote, key, value)

    db.commit()
    db.refresh(lote)
    return lote

@router.delete("/lotes/{lote_id}")
def deletar_lote(
    lote_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    lote = db.query(Lote).filter(Lote.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")
    db.delete(lote)
    db.commit()
    return {"mensagem": "Lote excluído com sucesso"}
