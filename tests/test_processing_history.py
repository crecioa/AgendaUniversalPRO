"""Testes do histórico de processamento (Sprint 5.14)."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest
from docx import Document

from core.agenda_updater import AgendaUpdater
from services.processing_history import ProcessingHistoryService


def _updater(tmp_path: Path) -> AgendaUpdater:
    updater = AgendaUpdater()
    updater.backup_service.criar_backup = Mock()  # type: ignore[method-assign]
    updater.history_service = ProcessingHistoryService(tmp_path / "historico.jsonl")
    return updater


def _documento(caminho: Path, texto: str) -> None:
    documento = Document()
    documento.add_paragraph(texto)
    documento.save(str(caminho))


def test_historico_sucesso_e_acumulacao(tmp_path: Path) -> None:
    updater = _updater(tmp_path)
    origem = tmp_path / "origem.docx"
    _documento(origem, "05/01/2026")
    assert updater.atualizar_ano(origem, 2026, 2027, tmp_path / "ano.docx") == 1
    assert updater.atualizar_agenda(
        origem, {"05/01/2026": "05/01/2028"}, tmp_path / "datas.docx"
    ) == 1
    registros = updater.history_service.consultar()
    assert len(registros) == 2
    assert [r["operacao"] for r in registros] == ["ano", "substituicoes"]
    assert all(r["status"] == "sucesso" for r in registros)
    assert all(r["atualizadas"] == 1 for r in registros)


def test_historico_falha_sem_publicacao(tmp_path: Path) -> None:
    updater = _updater(tmp_path)
    origem = tmp_path / "origem.docx"
    destino = tmp_path / "destino.docx"
    _documento(origem, "29/02/2024")
    with pytest.raises(ValueError, match="Validação de conteúdo falhou"):
        updater.atualizar_ano(origem, 2024, 2025, destino)
    assert not destino.exists()
    registro = updater.history_service.consultar()[0]
    assert registro["status"] == "falha"
    assert "ValueError" in str(registro["erro"])


def test_historico_exportacao(tmp_path: Path) -> None:
    updater = _updater(tmp_path)
    origem = tmp_path / "origem.docx"
    _documento(origem, "05/01/2026")
    updater.atualizar_ano(origem, 2026, 2027, tmp_path / "destino.docx")
    relatorio = tmp_path / "relatorio.json"
    assert updater.exportar_ultimo_relatorio(relatorio) == relatorio
    eventos = updater.history_service.consultar()
    assert len(eventos) == 2
    assert eventos[1]["operacao"] == "exportacao_relatorio"
    assert eventos[1]["relatorio"] == str(relatorio)


def test_historico_nao_impede_publicacao_se_falhar(tmp_path: Path) -> None:
    updater = _updater(tmp_path)
    updater.history_service.registrar = Mock(side_effect=OSError("disco"))  # type: ignore[method-assign]
    origem = tmp_path / "origem.docx"
    destino = tmp_path / "destino.docx"
    _documento(origem, "05/01/2026")
    assert updater.atualizar_ano(origem, 2026, 2027, destino) == 1
    assert destino.exists()


def test_consultar_inexistente(tmp_path: Path) -> None:
    assert ProcessingHistoryService(tmp_path / "nao_existe.jsonl").consultar() == []


def test_registro_json_utf8_e_sem_sobrescrita(tmp_path: Path) -> None:
    caminho = tmp_path / "historico.jsonl"
    servico = ProcessingHistoryService(caminho)
    servico.registrar(operacao="ano", origem="Audiência.docx", destino="saída.docx", status="sucesso")
    servico.registrar(operacao="ano", origem="outro.docx", destino="novo.docx", status="falha")
    linhas = caminho.read_text(encoding="utf-8").splitlines()
    assert len(linhas) == 2
    assert json.loads(linhas[0])["origem"] == "Audiência.docx"
    assert json.loads(linhas[1])["status"] == "falha"


def test_status_invalido_nao_cria_arquivo(tmp_path: Path) -> None:
    caminho = tmp_path / "historico.jsonl"
    with pytest.raises(ValueError, match="Status"):
        ProcessingHistoryService(caminho).registrar(
            operacao="ano", origem="a", destino="b", status="desconhecido"
        )
    assert not caminho.exists()
