"""Testes das exportações estatísticas JSON e CSV (Sprint 5.17)."""

import csv
import json
from datetime import date
from pathlib import Path

import pytest

from services.processing_history import ProcessingHistoryService


def _servico(tmp_path: Path) -> ProcessingHistoryService:
    servico = ProcessingHistoryService(tmp_path / "histórico.jsonl")
    servico.registrar(
        operacao="ano", origem="Audiência.docx", destino="saída.docx",
        status="sucesso", atualizadas=3,
    )
    servico.registrar(
        operacao="substituicoes", origem="entrada.docx", destino="saída.docx",
        status="falha",
    )
    servico.registrar(
        operacao="exportacao_relatorio", origem="entrada.docx", destino="relatório.json",
        status="sucesso",
    )
    return servico


def test_json_contem_resumo_e_distribuicao(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "resumo.json"
    assert servico.exportar_resumo_json(destino) == destino
    dados = json.loads(destino.read_text(encoding="utf-8"))
    assert dados == servico.resumir()
    assert dados["por_operacao"]["ano"] == 1
    assert dados["datas_atualizadas"] == 3


def test_csv_contem_indicadores_e_distribuicao(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "resumo.csv"
    assert servico.exportar_resumo_csv(destino) == destino
    with destino.open(encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    valores = {linha["indicador"]: linha["valor"] for linha in linhas}
    assert valores["total_operacoes"] == "3"
    assert valores["sucessos"] == "2"
    assert valores["falhas"] == "1"
    assert valores["datas_atualizadas"] == "3"
    assert valores["por_operacao:substituicoes"] == "1"


@pytest.mark.parametrize("formato", ["json", "csv"])
def test_exportacao_com_filtros(tmp_path: Path, formato: str) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / f"filtrado.{formato}"
    exportar = servico.exportar_resumo_json if formato == "json" else servico.exportar_resumo_csv
    exportar(destino, status="sucesso", operacao="ano")
    if formato == "json":
        dados = json.loads(destino.read_text(encoding="utf-8"))
        assert dados["total_operacoes"] == 1
        assert dados["datas_atualizadas"] == 3
    else:
        with destino.open(encoding="utf-8-sig", newline="") as arquivo:
            valores = {linha["indicador"]: linha["valor"] for linha in csv.DictReader(arquivo)}
        assert valores["total_operacoes"] == "1"
        assert valores["datas_atualizadas"] == "3"


@pytest.mark.parametrize("formato", ["json", "csv"])
def test_nao_sobrescreve(tmp_path: Path, formato: str) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / f"resumo.{formato}"
    destino.write_bytes(b"preservar")
    exportar = servico.exportar_resumo_json if formato == "json" else servico.exportar_resumo_csv
    with pytest.raises(FileExistsError):
        exportar(destino)
    assert destino.read_bytes() == b"preservar"


@pytest.mark.parametrize("formato", ["json", "csv"])
def test_historico_vazio(tmp_path: Path, formato: str) -> None:
    servico = ProcessingHistoryService(tmp_path / "inexistente.jsonl")
    destino = tmp_path / f"vazio.{formato}"
    if formato == "json":
        servico.exportar_resumo_json(destino)
        assert json.loads(destino.read_text(encoding="utf-8"))["total_operacoes"] == 0
    else:
        servico.exportar_resumo_csv(destino)
        with destino.open(encoding="utf-8-sig", newline="") as arquivo:
            valores = {linha["indicador"]: linha["valor"] for linha in csv.DictReader(arquivo)}
        assert valores["total_operacoes"] == "0"
        assert "por_operacao:ano" not in valores
    assert not servico.caminho.exists()


@pytest.mark.parametrize("formato", ["json", "csv"])
def test_exportacao_nao_altera_historico(tmp_path: Path, formato: str) -> None:
    servico = _servico(tmp_path)
    original = servico.caminho.read_bytes()
    destino = tmp_path / f"resumo.{formato}"
    if formato == "json":
        servico.exportar_resumo_json(destino)
    else:
        servico.exportar_resumo_csv(destino)
    assert servico.caminho.read_bytes() == original


@pytest.mark.parametrize("formato", ["json", "csv"])
def test_filtro_invalido_nao_cria_arquivo(tmp_path: Path, formato: str) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / f"resumo.{formato}"
    exportar = servico.exportar_resumo_json if formato == "json" else servico.exportar_resumo_csv
    with pytest.raises(ValueError, match="Status"):
        exportar(destino, status="pendente")
    assert not destino.exists()


@pytest.mark.parametrize("formato", ["json", "csv"])
def test_extensao_invalida(tmp_path: Path, formato: str) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "resumo.txt"
    exportar = servico.exportar_resumo_json if formato == "json" else servico.exportar_resumo_csv
    with pytest.raises(ValueError, match="extensão"):
        exportar(destino)
    assert not destino.exists()


def test_json_utf8_preserva_acentos(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    servico.registrar(operacao="revisão", origem="a", destino="b", status="sucesso")
    destino = tmp_path / "resumo.json"
    servico.exportar_resumo_json(destino)
    assert '"revisão"' in destino.read_text(encoding="utf-8")


def test_csv_utf8_bom_para_excel(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    servico.registrar(operacao="revisão", origem="a", destino="b", status="sucesso")
    destino = tmp_path / "resumo.csv"
    servico.exportar_resumo_csv(destino)
    assert destino.read_bytes().startswith(b"\xef\xbb\xbf")
    with destino.open(encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    assert any(linha["indicador"] == "por_operacao:revisão" for linha in linhas)


def test_filtro_periodo_sem_registros(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "resumo.json"
    servico.exportar_resumo_json(destino, inicio=date(2000, 1, 1), fim=date(2000, 1, 2))
    assert json.loads(destino.read_text(encoding="utf-8"))["total_operacoes"] == 0
