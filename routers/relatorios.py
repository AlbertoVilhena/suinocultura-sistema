from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from utils.deps import get_db
from utils.security import usuario_logado
from models.lote import Lote
from models.pesagem import Pesagem
from models.alimentacao import Alimentacao
from datetime import date

router = APIRouter()

@router.get("/relatorios/lotes/{lote_id}")
def relatorio_lote(lote_id: int, db: Session = Depends(get_db), usuario: str = Depends(usuario_logado)):
    lote = db.query(Lote).filter(Lote.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")

    pesagens = db.query(Pesagem).filter(Pesagem.lote_id == lote_id).order_by(Pesagem.data_pesagem).all()
    alimentacoes = db.query(Alimentacao).filter(Alimentacao.lote_id == lote_id).all()

    total_pesagens = len(pesagens)
    ultimo_peso = pesagens[-1].peso_medio if pesagens else None
    total_racao = sum([a.quantidade_kg for a in alimentacoes])
    dias_corridos = (date.today() - lote.data_inicio).days or 1

    estimativa_ganho_diario = round(ultimo_peso / dias_corridos, 2) if ultimo_peso else None

    return {
        "lote_id": lote.id,
        "nome": lote.nome,
        "data_inicio": lote.data_inicio,
        "total_pesagens": total_pesagens,
        "ultimo_peso_medio": ultimo_peso,
        "total_racao_kg": round(total_racao, 2),
        "dias_corridos": dias_corridos,
        "peso_medio_por_dia": estimativa_ganho_diario,
    }
