from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.database import Base, engine
from models import usuario, lote, pesagem  # importa todos os models
from routers import usuarios, lotes, pesagens  # importa todos os routers
from routers import alimentacoes
from models import alimentacao
from routers import vacinacoes
from models import vacinacao
from routers import relatorios
app.include_router(relatorios.router)



# Criação do app deve vir antes de qualquer uso do app
app = FastAPI()

# Middleware CORS (libera acesso externo ao backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina origens específicas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Criação das tabelas no banco
Base.metadata.create_all(bind=engine)

# Rotas (routers)
app.include_router(usuarios.router)
app.include_router(lotes.router)
app.include_router(pesagens.router)
app.include_router(alimentacoes.router)  # 👈 Aqui entra o router de alimentação


# Rota de saúde
@app.get("/")
def root():
    return {"status": "ok"}
    
Base.metadata.create_all(bind=engine)
app.include_router(vacinacoes.router)

