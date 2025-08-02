from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from utils.database import Base

class Pesagem(Base):
    __tablename__ = "pesagens"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"), nullable=False)
    peso_medio = Column(Float, nullable=False)
    data_pesagem = Column(Date, nullable=False)
    observacoes = Column(String)

    lote = relationship("Lote", backref="pesagens")
