from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from utils.database import Base

class Vacinacao(Base):
    __tablename__ = "vacinacoes"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lotes.id"), nullable=False)
    vacina_nome = Column(String, nullable=False)
    data_aplicacao = Column(Date, nullable=False)
    responsavel = Column(String, nullable=False)
    observacoes = Column(String)

    lote = relationship("Lote", backref="vacinacoes")
