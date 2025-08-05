from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils.deps import get_db
from utils.security import fake_hash, fake_verify, criar_token, usuario_logado
from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioLogin, UsuarioOut

router = APIRouter()

# Criar novo usuário
@router.post("/usuarios", response_model=UsuarioOut)
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="E-mail já está em uso")

    novo = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=fake_hash(usuario.senha)
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

# Login e geração de token
@router.post("/login")
def login(dados: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == dados.email).first()
    if not user or not fake_verify(dados.senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token(user.email)
    return {"access_token": token, "token_type": "bearer"}

# Obter dados do usuário logado
@router.get("/me", response_model=UsuarioOut)
def get_me(db: Session = Depends(get_db), email: str = Depends(usuario_logado)):
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
