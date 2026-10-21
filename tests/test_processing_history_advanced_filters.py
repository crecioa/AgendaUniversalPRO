"""Filtros exatos de origem e destino em consultas e exportações (Sprint 5.19)."""

import csv
import json
from pathlib import Path

import pytest

from services.processing_history import ProcessingHistoryService


def _servico(tmp_path: Path) -> ProcessingHistoryService:
    servico = ProcessingHistoryService(tmp_path / "historico.jsonl")
    for origem, destino, status, atualizadas in (
        ("Audiência.docx", "saída.docx", "sucesso", 3),
        ("Audiência.docx", "outra.docx", "falha", None),
        ("entrada.docx", "saída.docx", "sucesso", 2),
    ):
        servico.registrar(
            operacao="ano", origem=origem, destino=destino,
            status=status, atualizadas=atualizadas,
        )
    return servico


def test_consulta_por_origem(tmp_path: Path) -> None:
    assert len(_servico(tmp_path).consultar(origem="Audiência.docx")) == 2


def test_consulta_por_destino(tmp_path: Path) -> None:
    assert len(_servico(tmp_path).consultar(arquivo_destino="saída.docx")) == 2


def test_consulta_combinada(tmp_path: Path) -> None:
    registros = _servico(tmp_path).consultar(
        origem="Audiência.docx", arquivo_destino="saída.docx", status="sucesso"
    )
    assert len(registros) == 1
    assert registros[0]["atualizadas"] == 3


def test_consulta_sem_correspondencia(tmp_path: Path) -> None:
    assert _servico(tmp_path).consultar(origem="inexistente.docx") == []


def test_consulta_caminho_path(tmp_path: Path) -> None:
    assert len(_servico(tmp_path).consultar(origem=Path("Audiência.docx"))) == 2


def test_consulta_diferencia_maiusculas(tmp_path: Path) -> None:
    assert _servico(tmp_path).consultar(origem="audiência.docx") == []


@pytest.mark.parametrize("campo", ["origem", "arquivo_destino"])
@pytest.mark.parametrize("valor", ["", "   "])
def test_filtro_vazio_invalido(tmp_path: Path, campo: str, valor: str) -> None:
    with pytest.raises(ValueError, match="inválido"):
        servico = _servico(tmp_path)
        if campo == "origem":
            servico.consultar(origem=valor)
        else:
            servico.consultar(arquivo_destino=valor)


def test_resumo_respeita_filtros(tmp_path: Path) -> None:
    resumo = _servico(tmp_path).resumir(origem="Audiência.docx", arquivo_destino="saída.docx")
    assert resumo["total_operacoes"] == 1
    assert resumo["datas_atualizadas"] == 3


def test_csv_historico_respeita_filtros(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "historico.csv"
    servico.exportar_csv(destino, origem="Audiência.docx", arquivo_destino="saída.docx")
    with destino.open(encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    assert len(linhas) == 1
    assert linhas[0]["origem"] == "Audiência.docx"


def test_resumo_json_respeita_filtros(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "resumo.json"
    servico.exportar_resumo_json(destino, arquivo_destino="outra.docx")
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["total_operacoes"] == 1
    assert dados["falhas"] == 1


def test_resumo_csv_respeita_filtros(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "resumo.csv"
    servico.exportar_resumo_csv(destino, origem="entrada.docx")
    with destino.open(encoding="utf-8-sig", newline="") as arquivo:
        valores = {r["indicador"]: r["valor"] for r in csv.DictReader(arquivo)}
    assert valores["total_operacoes"] == "1"
    assert valores["datas_atualizadas"] == "2"


def test_consolidado_filtros_e_auditoria(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "consolidado.json"
    servico.exportar_relatorio_consolidado(
        destino, origem="Audiência.docx", arquivo_destino="saída.docx"
    )
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados["auditoria"]["filtros"]["origem"] == "Audiência.docx"
    assert dados["auditoria"]["filtros"]["arquivo_destino"] == "saída.docx"
    assert dados["auditoria"]["quantidade_registros"] == 1
    assert dados["resumo"]["total_operacoes"] == 1
    assert len(dados["registros"]) == 1


def test_exportacao_filtro_invalido_nao_cria_arquivo(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "consolidado.json"
    with pytest.raises(ValueError, match="inválido"):
        servico.exportar_relatorio_consolidado(destino, origem="")
    assert not destino.exists()


def test_exportacao_nao_sobrescreve(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "consolidado.json"
    destino.write_text("preservar", encoding="utf-8")
    with pytest.raises(FileExistsError):
        servico.exportar_relatorio_consolidado(destino, origem="Audiência.docx")
    assert destino.read_text(encoding="utf-8") == "preservar"


def test_consulta_e_exportacao_preservam_historico(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    original = servico.caminho.read_bytes()
    servico.consultar(origem="Audiência.docx")
    servico.exportar_relatorio_consolidado(tmp_path / "relatorio.json", origem="Audiência.docx")
    assert servico.caminho.read_bytes() == original
