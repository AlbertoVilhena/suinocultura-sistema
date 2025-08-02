from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from utils.database import Base

class Alimentacao(Base):
    __tablename__ = "alimentacoes"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"), nullable=False)
    tipo_racao = Column(String, nullable=False)
    quantidade_kg = Column(Float, nullable=False)
    data_fornecida = Column(Date, nullable=False)
    observacoes = Column(String)

    lote = relationship("Lote", backref="alimentacoes")
