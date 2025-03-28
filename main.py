from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import usuarios, lotes

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
