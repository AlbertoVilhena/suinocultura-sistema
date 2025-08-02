from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

# CONFIGURAÇÕES
SECRET_KEY = "chave-muito-secreta-troque-isso"  # troque por algo seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hora

# CONTEXTO PARA HASH DE SENHA
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# FUNÇÃO PARA CRIAR HASH
def fake_hash(senha: str) -> str:
    return pwd_context.hash(senha)

# FUNÇÃO PARA VERIFICAR SENHA
def fake_verify(senha: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha, senha_hash)

# FUNÇÃO PARA CRIAR TOKEN JWT
def criar_token(email: str) -> str:
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": email, "exp": expira}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# FUNÇÃO PARA VALIDAR TOKEN JWT
def validar_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except JWTError:
        return None
