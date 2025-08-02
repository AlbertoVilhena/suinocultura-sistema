from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .auth import validar_token

# Essa URL é usada para identificar onde o usuário fará login (tokenUrl)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def usuario_logado(token: str = Depends(oauth2_scheme)) -> str:
    """
    Função que valida o token e retorna o e-mail do usuário autenticado.
    Se o token for inválido ou expirado, retorna erro 401.
    """
    email = validar_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return email  # pode ser retornado o email ou até um objeto usuário
