from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.auth import fake_hash, fake_verify, criar_token, usuarios_db

router = APIRouter()

class Usuario(BaseModel):
    email: str
    senha: str

@router.post("/usuarios")
def criar_usuario(usuario: Usuario):
    if usuario.email in usuarios_db:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    usuarios_db[usuario.email] = {
        "email": usuario.email,
        "senha": fake_hash(usuario.senha)
    }
    return {"mensagem": "Usuário criado com sucesso"}

@router.post("/login")
def login(usuario: Usuario):
    user = usuarios_db.get(usuario.email)
    if not user or not fake_verify(usuario.senha, user["senha"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    token = criar_token(usuario.email)
    return {"token": token}
