from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Lote(Base):
    __tablename__ = "lotes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    quantidade = Column(Integer)
    data_entrada = Column(Date)
    fase_atual = Column(String)
    ativo = Column(Boolean, default=True)

class Pesagem(Base):
    __tablename__ = "pesagens"
    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"))
    data = Column(Date)
    peso_total_kg = Column(Float)

class Estoque(Base):
    __tablename__ = "estoque"
    id = Column(Integer, primary_key=True, index=True)
    ingrediente = Column(String)
    quantidade_kg = Column(Float)
    preco_unitario = Column(Float)
    tipo = Column(String)
    data_atualizacao = Column(Date)

class RecomendacaoIA(Base):
    __tablename__ = "ia"
    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"))
    data = Column(Date)
    recomendacao = Column(String)
    motivacao = Column(String)
