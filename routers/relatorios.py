from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from utils.deps import get_db
from utils.security import usuario_logado
from models.lote import Lote
from models.pesagem import Pesagem
from models.alimentacao import Alimentacao
from datetime import date, datetime
from fpdf import FPDF

router = APIRouter()

def gerar_pdf_individual(lote_info: dict) -> FileResponse:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Relatório do Lote {lote_info['Nome']} (ID {lote_info['Lote ID']})", ln=True, align="C")
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.ln(10)

    for key, label in [
        ("Data de Início", "Data de Início"),
        ("Total de Pesagens", "Total de Pesagens"),
        ("Último Peso Médio", "Último Peso Médio (kg)"),
        ("Total Ração (kg)", "Total de Ração (kg)"),
        ("Dias Corridos", "Dias Corridos"),
        ("Peso Médio/Dia", "Peso Médio por Dia (kg)"),
    ]:
        pdf.cell(0, 10, f"{label}: {lote_info[key]}", ln=True)

    path = f"/mnt/data/relatorio_lote_{lote_info['Lote ID']}.pdf"
    pdf.output(path)
    return FileResponse(path, media_type="application/pdf", filename=f"relatorio_lote_{lote_info['Lote ID']}.pdf")


@router.get("/relatorios/lotes/{lote_id}")
def relatorio_lote(
    lote_id: int,
    formato: str = Query("json", enum=["json", "pdf"]),
    db: Session = Depends(get_db),
    usuario: str = Depends(usuario_logado)
):
    lote = db.query(Lote).filter(Lote.id == lote_id).first()
    if not lote:
        raise HTTPException(status_code=404, detail="Lote não encontrado")

    pesagens = db.query(Pesagem).filter(Pesagem.lote_id == lote_id).order_by(Pesagem.data).all()
    alimentacoes = db.query(Alimentacao).filter(Alimentacao.lote_id == lote_id).all()

    total_pesagens = len(pesagens)
    ultimo_peso = pesagens[-1].peso_medio if pesagens else 0
    total_racao = sum([a.quantidade_kg for a in alimentacoes])
    dias_corridos = (date.today() - lote.data_inicio).days or 1
    estimativa_ganho_diario = round(ultimo_peso / dias_corridos, 2) if ultimo_peso else 0

    lote_info = {
        "Lote ID": lote.id,
        "Nome": lote.nome,
        "Data de Início": str(lote.data_inicio),
        "Total de Pesagens": total_pesagens,
        "Último Peso Médio": round(ultimo_peso, 2),
        "Total Ração (kg)": round(total_racao, 2),
        "Dias Corridos": dias_corridos,
        "Peso Médio/Dia": estimativa_ganho_diario,
    }

    if formato == "pdf":
        return gerar_pdf_individual(lote_info)

    return lote_info

