from fastapi import FastAPI
from app.routers import lotes, pesagens, estoque, ia

app = FastAPI()

app.include_router(lotes.router)
app.include_router(pesagens.router)
app.include_router(estoque.router)
app.include_router(ia.router)
