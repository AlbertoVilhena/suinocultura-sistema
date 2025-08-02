from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from utils.auth import fake_hash, fake_verify, criar_token
from utils.deps import get_db
from models.usuario import Usuario as UsuarioModel

router = APIRouter()

class Usuario(BaseModel):
    email: str
    senha: str

@router.post("/usuarios")
def criar_usuario(usuario: Usuario, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    novo_usuario = UsuarioModel(
        email=usuario.email,
        senha=fake_hash(usuario.senha)
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"mensagem": "Usuário criado com sucesso"}

@router.post("/login")
def login(usuario: Usuario, db: Session = Depends(get_db)):
    user = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if not user or not fake_verify(usuario.senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token(usuario.email)
    return {"token": token}
