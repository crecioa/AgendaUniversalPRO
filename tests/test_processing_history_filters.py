"""Testes dos filtros e da exportação do histórico (Sprint 5.15)."""

import csv
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from services.processing_history import ProcessingHistoryService


def _servico(tmp_path: Path) -> ProcessingHistoryService:
    servico = ProcessingHistoryService(tmp_path / "historico.jsonl")
    for operacao, status, data in (
        ("ano", "sucesso", "2026-10-19T23:30:00+00:00"),
        ("substituicoes", "falha", "2026-10-20T12:00:00+00:00"),
        ("ano", "sucesso", "2026-10-21T00:00:00+00:00"),
    ):
        servico.registrar(operacao=operacao, origem="origem.docx", destino="destino.docx", status=status)
    linhas = servico.caminho.read_text(encoding="utf-8").splitlines()
    eventos = [json.loads(linha) for linha in linhas]
    for evento, (_, _, data) in zip(eventos, (
        ("ano", "sucesso", "2026-10-19T23:30:00+00:00"),
        ("substituicoes", "falha", "2026-10-20T12:00:00+00:00"),
        ("ano", "sucesso", "2026-10-21T00:00:00+00:00"),
    )):
        evento["data_hora_utc"] = data
    servico.caminho.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in eventos), encoding="utf-8")
    return servico


def test_filtro_status(tmp_path: Path) -> None:
    registros = _servico(tmp_path).consultar(status="falha")
    assert len(registros) == 1
    assert registros[0]["operacao"] == "substituicoes"


def test_filtro_operacao(tmp_path: Path) -> None:
    assert len(_servico(tmp_path).consultar(operacao="ano")) == 2


def test_filtro_datas_inclusivo(tmp_path: Path) -> None:
    registros = _servico(tmp_path).consultar(inicio=date(2026, 10, 20), fim=date(2026, 10, 20))
    assert len(registros) == 1
    assert registros[0]["status"] == "falha"


def test_filtros_combinados(tmp_path: Path) -> None:
    registros = _servico(tmp_path).consultar(
        inicio=date(2026, 10, 20), status="sucesso", operacao="ano"
    )
    assert len(registros) == 1
    data_hora = registros[0]["data_hora_utc"]
    assert isinstance(data_hora, str)
    assert data_hora.startswith("2026-10-21")


def test_filtro_datetime_com_fuso(tmp_path: Path) -> None:
    fuso = timezone(timedelta(hours=-3))
    instante = datetime(2026, 10, 20, 9, 0, tzinfo=fuso)
    registros = _servico(tmp_path).consultar(inicio=instante, fim=instante)
    assert len(registros) == 1


def test_filtros_invalidos(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    with pytest.raises(ValueError, match="início"):
        servico.consultar(inicio=date(2026, 10, 22), fim=date(2026, 10, 20))
    with pytest.raises(ValueError, match="Status"):
        servico.consultar(status="desconhecido")
    with pytest.raises(ValueError, match="fuso"):
        servico.consultar(inicio=datetime(2026, 10, 20))


def test_exportar_csv_com_filtros_e_utf8(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "histórico.csv"
    original = servico.caminho.read_bytes()
    assert servico.exportar_csv(destino, status="sucesso") == destino
    with destino.open(encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    assert len(linhas) == 2
    assert all(linha["status"] == "sucesso" for linha in linhas)
    assert servico.caminho.read_bytes() == original


def test_csv_nao_sobrescreve(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    destino = tmp_path / "historico.csv"
    destino.write_text("preservar", encoding="utf-8")
    with pytest.raises(FileExistsError):
        servico.exportar_csv(destino)
    assert destino.read_text(encoding="utf-8") == "preservar"


def test_csv_sem_registros_tem_cabecalho(tmp_path: Path) -> None:
    servico = ProcessingHistoryService(tmp_path / "ausente.jsonl")
    destino = tmp_path / "vazio.csv"
    servico.exportar_csv(destino)
    with destino.open(encoding="utf-8-sig", newline="") as arquivo:
        linhas = list(csv.reader(arquivo))
    assert len(linhas) == 1
    assert "data_hora_utc" in linhas[0]


def test_registro_invalido_informa_linha(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    with servico.caminho.open("a", encoding="utf-8") as arquivo:
        arquivo.write("{invalido}\n")
    with pytest.raises(ValueError, match="linha 4"):
        servico.consultar()
    assert not (tmp_path / "falha.csv").exists()
    with pytest.raises(ValueError, match="linha 4"):
        servico.exportar_csv(tmp_path / "falha.csv")
    assert not (tmp_path / "falha.csv").exists()
