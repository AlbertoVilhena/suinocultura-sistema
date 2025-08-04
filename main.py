from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.database import Base, engine
from models import usuario, lote, pesagem, alimentacao, vacinacao
from routers import usuarios, lotes, pesagens, alimentacoes, vacinacoes, relatorios

# ✅ Criação da aplicação
app = FastAPI()

# ✅ Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Criação de todas as tabelas
Base.metadata.create_all(bind=engine)

# ✅ Registro de rotas
app.include_router(usuarios.router)
app.include_router(lotes.router)
app.include_router(pesagens.router)
app.include_router(alimentacoes.router)
app.include_router(vacinacoes.router)
app.include_router(relatorios.router)  # 👈 Aqui entra o módulo de relatórios

# ✅ Rota de teste
@app.get("/")
def root():
    return {"status": "ok"}

