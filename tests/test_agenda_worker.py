"""Testes do AgendaWorker."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from config.agenda_config import AgendaConfig
from ui.agenda_worker import AgendaWorker


def criar_config() -> AgendaConfig:
    return AgendaConfig(
        arquivo_origem=Path("origem.docx"),
        arquivo_destino=Path("destino.docx"),
        ano_origem=2026,
        ano_destino=2027,
    )


def test_worker_emite_sucesso() -> None:
    worker = AgendaWorker(criar_config())

    resultados: list[int] = []
    erros: list[str] = []

    worker.sucesso.connect(resultados.append)
    worker.erro.connect(erros.append)

    with patch(
        "ui.agenda_worker.AgendaApplication"
    ) as aplicacao_mock:
        aplicacao_mock.return_value.atualizar.return_value = 15
        worker.run()

    assert resultados == [15]
    assert erros == []


def test_worker_emite_erro() -> None:
    worker = AgendaWorker(criar_config())

    resultados: list[int] = []
    erros: list[str] = []

    worker.sucesso.connect(resultados.append)
    worker.erro.connect(erros.append)

    with patch(
        "ui.agenda_worker.AgendaApplication"
    ) as aplicacao_mock:
        aplicacao_mock.return_value.atualizar.side_effect = ValueError(
            "Documento inválido"
        )
        worker.run()

    assert resultados == []
    assert erros == ["Documento inválido"]