from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.deps import get_db
from utils.security import usuario_logado
from models.vacinacao import Vacinacao
from models.lote import Lote
from schemas import vacinacao as schemas

router = APIRouter()

@router.post("/vacinacoes", response_model=schemas.VacinacaoOut)
def criar_vacinacao(v: schemas.VacinacaoCreate, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    lote = db.query(Lote).filter(Lote.id == v.lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")

    nova = Vacinacao(**v.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.get("/vacinacoes", response_model=list[schemas.VacinacaoOut])
def listar_vacinacoes(db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    return db.query(Vacinacao).all()

@router.get("/vacinacoes/{vacinacao_id}", response_model=schemas.VacinacaoOut)
def buscar_vacinacao(vacinacao_id: int, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    vac = db.query(Vacinacao).filter(Vacinacao.id == vacinacao_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return vac

@router.put("/vacinacoes/{vacinacao_id}", response_model=schemas.VacinacaoOut)
def atualizar_vacinacao(vacinacao_id: int, dados: schemas.VacinacaoUpdate, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    vac = db.query(Vacinacao).filter(Vacinacao.id == vacinacao_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    for key, value in dados.dict().items():
        setattr(vac, key, value)

    db.commit()
    db.refresh(vac)
    return vac

@router.delete("/vacinacoes/{vacinacao_id}")
def deletar_vacinacao(vacinacao_id: int, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    vac = db.query(Vacinacao).filter(Vacinacao.id == vacinacao_id).first()
    if not vac:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    db.delete(vac)
    db.commit()
    return {"mensagem": "Registro de vacinação excluído com sucesso"}
