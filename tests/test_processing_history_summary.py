"""Testes do resumo estatístico do histórico (Sprint 5.16)."""

import json
from datetime import date
from pathlib import Path

import pytest

from services.processing_history import ProcessingHistoryService


def _servico(tmp_path: Path) -> ProcessingHistoryService:
    servico = ProcessingHistoryService(tmp_path / "historico.jsonl")
    eventos = [
        ("ano", "sucesso", 3, "2026-10-19T10:00:00+00:00"),
        ("substituicoes", "sucesso", 2, "2026-10-20T10:00:00+00:00"),
        ("ano", "falha", None, "2026-10-20T12:00:00+00:00"),
        ("exportacao_relatorio", "sucesso", 3, "2026-10-21T10:00:00+00:00"),
    ]
    for operacao, status, atualizadas, _ in eventos:
        servico.registrar(
            operacao=operacao, origem="origem.docx", destino="destino.docx",
            status=status, atualizadas=atualizadas,
        )
    linhas = [json.loads(linha) for linha in servico.caminho.read_text(encoding="utf-8").splitlines()]
    for registro, (_, _, _, instante) in zip(linhas, eventos):
        registro["data_hora_utc"] = instante
    servico.caminho.write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in linhas),
        encoding="utf-8",
    )
    return servico


def test_resumo_total_e_distribuicao(tmp_path: Path) -> None:
    resumo = _servico(tmp_path).resumir()
    assert resumo["total_operacoes"] == 4
    assert resumo["sucessos"] == 3
    assert resumo["falhas"] == 1
    assert resumo["taxa_sucesso_percentual"] == 75.0
    assert resumo["por_operacao"] == {"ano": 2, "substituicoes": 1, "exportacao_relatorio": 1}


def test_atualizacoes_nao_duplicam_exportacao(tmp_path: Path) -> None:
    resumo = _servico(tmp_path).resumir()
    assert resumo["atualizacoes_documentos"] == 2
    assert resumo["datas_atualizadas"] == 5


def test_filtro_periodo_inclusivo(tmp_path: Path) -> None:
    resumo = _servico(tmp_path).resumir(inicio=date(2026, 10, 20), fim=date(2026, 10, 20))
    assert resumo["total_operacoes"] == 2
    assert resumo["sucessos"] == 1
    assert resumo["falhas"] == 1


def test_filtro_status(tmp_path: Path) -> None:
    resumo = _servico(tmp_path).resumir(status="falha")
    assert resumo["total_operacoes"] == 1
    assert resumo["taxa_sucesso_percentual"] == 0.0
    assert resumo["datas_atualizadas"] == 0


def test_filtro_operacao(tmp_path: Path) -> None:
    resumo = _servico(tmp_path).resumir(operacao="ano")
    assert resumo["total_operacoes"] == 2
    assert resumo["datas_atualizadas"] == 3


def test_historico_vazio(tmp_path: Path) -> None:
    resumo = ProcessingHistoryService(tmp_path / "ausente.jsonl").resumir()
    assert resumo == {
        "total_operacoes": 0, "sucessos": 0, "falhas": 0,
        "taxa_sucesso_percentual": 0.0, "atualizacoes_documentos": 0,
        "datas_atualizadas": 0, "por_operacao": {},
    }


def test_resumo_nao_modifica_historico(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    original = servico.caminho.read_bytes()
    servico.resumir()
    assert servico.caminho.read_bytes() == original


def test_resumo_rejeita_filtro_invalido(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Status"):
        _servico(tmp_path).resumir(status="pendente")


def test_resumo_rejeita_quantidade_invalida(tmp_path: Path) -> None:
    servico = _servico(tmp_path)
    linhas = servico.caminho.read_text(encoding="utf-8").splitlines()
    evento = json.loads(linhas[0])
    evento["atualizadas"] = -1
    linhas[0] = json.dumps(evento)
    servico.caminho.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="Quantidade atualizada inválida"):
        servico.resumir()
