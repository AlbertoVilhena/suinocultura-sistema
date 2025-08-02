from sqlalchemy import Column, Integer, String, Date
from utils.database import Base

class Lote(Base):
    __tablename__ = "lotes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    data_inicio = Column(Date, nullable=False)
    tipo_racao = Column(String, nullable=False)
