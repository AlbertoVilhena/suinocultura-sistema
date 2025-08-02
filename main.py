from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import usuarios, lotes
from utils.database import Base, engine
from models import usuario, lote
from routers import pesagens  # já deve existir lotes, usuarios, etc.
from models import pesagem  # além de usuario, lote, etc.

Base.metadata.create_all(bind=engine)

app.include_router(pesagens.router)


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios.router)
app.include_router(lotes.router)
@app.get("/")
def root():
    return {"status": "ok"}

