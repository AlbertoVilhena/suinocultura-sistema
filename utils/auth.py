from fastapi import Header, HTTPException
import hashlib
import uuid

usuarios_db = {}

def fake_hash(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()

def fake_verify(senha: str, senha_hash: str) -> bool:
    return fake_hash(senha) == senha_hash

tokens = {}

def criar_token(email: str) -> str:
    token = str(uuid.uuid4())
    tokens[token] = email
    return token

def verificar_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Token inválido")
    token = authorization.replace("Bearer ", "")
    if token not in tokens:
        raise HTTPException(status_code=403, detail="Token expirado ou inválido")
    return tokens[token]
