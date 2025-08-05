from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.deps import get_db
from utils.auth import get_current_user  # ✅ autenticação JWT
from models.pesagem import Pesagem
from models.lote import Lote
from schemas import pesagem as schemas

router = APIRouter()

@router.post("/pesagens", response_model=schemas.PesagemOut)
def criar_pesagem(
    pesagem: schemas.PesagemCreate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    lote = db.query(Lote).filter(Lote.id == pesagem.lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")

    nova = Pesagem(**pesagem.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova

@router.get("/pesagens", response_model=list[schemas.PesagemOut])
def listar_pesagens(
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    return db.query(Pesagem).all()

@router.get("/pesagens/{pesagem_id}", response_model=schemas.PesagemOut)
def buscar_pesagem(
    pesagem_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    pesagem = db.query(Pesagem).filter(Pesagem.id == pesagem_id).first()
    if not pesagem:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    return pesagem

@router.put("/pesagens/{pesagem_id}", response_model=schemas.PesagemOut)
def atualizar_pesagem(
    pesagem_id: int,
    dados: schemas.PesagemUpdate,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    pesagem = db.query(Pesagem).filter(Pesagem.id == pesagem_id).first()
    if not pesagem:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    for key, value in dados.dict().items():
        setattr(pesagem, key, value)

    db.commit()
    db.refresh(pesagem)
    return pesagem

@router.delete("/pesagens/{pesagem_id}")
def deletar_pesagem(
    pesagem_id: int,
    db: Session = Depends(get_db),
    usuario: str = Depends(get_current_user)
):
    pesagem = db.query(Pesagem).filter(Pesagem.id == pesagem_id).first()
    if not pesagem:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    db.delete(pesagem)
    db.commit()
    return {"mensagem": "Registro de pesagem excluído com sucesso"}
