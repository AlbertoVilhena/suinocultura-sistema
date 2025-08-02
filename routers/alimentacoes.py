from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.deps import get_db
from utils.security import usuario_logado
from models.alimentacao import Alimentacao
from models.lote import Lote
from schemas import alimentacao as schemas

router = APIRouter()

@router.post("/alimentacoes", response_model=schemas.AlimentacaoOut)
def criar_alimentacao(al: schemas.AlimentacaoCreate, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    lote = db.query(Lote).filter(Lote.id == al.lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")

    nova = Alimentacao(**al.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.get("/alimentacoes", response_model=list[schemas.AlimentacaoOut])
def listar_alimentacoes(db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    return db.query(Alimentacao).all()

@router.get("/alimentacoes/{alimentacao_id}", response_model=schemas.AlimentacaoOut)
def buscar_alimentacao(alimentacao_id: int, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    al = db.query(Alimentacao).filter(Alimentacao.id == alimentacao_id).first()
    if not al:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return al

@router.put("/alimentacoes/{alimentacao_id}", response_model=schemas.AlimentacaoOut)
def atualizar_alimentacao(alimentacao_id: int, dados: schemas.AlimentacaoUpdate, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    al = db.query(Alimentacao).filter(Alimentacao.id == alimentacao_id).first()
    if not al:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    for key, value in dados.dict().items():
        setattr(al, key, value)

    db.commit()
    db.refresh(al)
    return al

@router.delete("/alimentacoes/{alimentacao_id}")
def deletar_alimentacao(alimentacao_id: int, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    al = db.query(Alimentacao).filter(Alimentacao.id == alimentacao_id).first()
    if not al:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    db.delete(al)
    db.commit()
    return {"mensagem": "Registro de alimentação excluído com sucesso"}
