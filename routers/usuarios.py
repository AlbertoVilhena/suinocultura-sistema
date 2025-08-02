from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils.deps import get_db
from models import usuario as models
from utils.auth import fake_hash, fake_verify, criar_token

router = APIRouter()

class Usuario(BaseModel):
    email: str
    senha: str

@router.post("/usuarios")
def criar_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    usuario_existente = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    novo_usuario = models.Usuario(
        email=usuario.email,
        senha=fake_hash(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"mensagem": "Usuário criado com sucesso"}

@router.post("/login")
def login(usuario: Usuario, db: Session = Depends(get_db)):
    user = db.query(models.Usuario).filter(models.Usuario.email == usuario.email).first()
    if not user or not fake_verify(usuario.senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token(usuario.email)
    return {"access_token": token, "token_type": "bearer"}
