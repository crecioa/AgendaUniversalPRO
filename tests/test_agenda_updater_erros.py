"""
Agenda Universal PRO
Arquivo: tests/test_agenda_updater_erros.py

Testes do tratamento de erros do AgendaUpdater.

Sprint 4.6:
- Valida propagação das exceções.
- Valida tratamento de erros durante abertura.
- Valida tratamento de erros durante atualização.
"""

from pathlib import Path
from typing import Any, cast
from unittest.mock import Mock

import pytest

from core.agenda_updater import AgendaUpdater


def criar_updater() -> AgendaUpdater:
    """Cria um AgendaUpdater com dependências simuladas."""

    updater = AgendaUpdater()

    updater.logger = Mock()
    updater.backup_service = Mock()
    updater.word_service = Mock()
    updater.text_updater = Mock()

    return updater


def test_abrir_agenda_registra_e_repropaga_erro(
    tmp_path: Path,
) -> None:
    """Valida erro ocorrido durante abertura do documento."""

    arquivo = tmp_path / "agenda.docx"
    arquivo.write_text(
        "arquivo inválido",
        encoding="utf-8",
    )

    updater = criar_updater()

    word_service = cast(Any, updater.word_service)
    logger = cast(Any, updater.logger)

    erro = RuntimeError("Erro ao abrir documento.")

    word_service.abrir_documento.side_effect = erro

    with pytest.raises(
        RuntimeError,
        match="Erro ao abrir documento.",
    ):
        updater.abrir_agenda(arquivo)

    logger.exception.assert_called_once()


def test_atualizar_agenda_registra_e_repropaga_erro(
    tmp_path: Path,
) -> None:
    """Valida erro ocorrido durante atualização."""

    arquivo = tmp_path / "agenda.docx"
    destino = tmp_path / "agenda_atualizada.docx"

    arquivo.write_text(
        "arquivo válido para teste",
        encoding="utf-8",
    )

    updater = criar_updater()

    word_service = cast(Any, updater.word_service)
    text_updater = cast(Any, updater.text_updater)
    logger = cast(Any, updater.logger)

    documento = Mock()

    word_service.abrir_documento.return_value = documento

    erro = RuntimeError("Erro durante atualização.")

    text_updater.atualizar_datas.side_effect = erro

    with pytest.raises(
        RuntimeError,
        match="Erro durante atualização.",
    ):
        updater.atualizar_agenda(
            arquivo=arquivo,
            substituicoes={
                "01/01/2026": "01/01/2027",
            },
            destino=destino,
        )

    logger.exception.assert_called_once()


def test_atualizar_ano_registra_e_repropaga_erro(
    tmp_path: Path,
) -> None:
    """Valida erro ocorrido durante atualização automática do ano."""

    arquivo = tmp_path / "agenda.docx"
    destino = tmp_path / "agenda_2027.docx"

    arquivo.write_text(
        "arquivo válido para teste",
        encoding="utf-8",
    )

    updater = criar_updater()

    word_service = cast(Any, updater.word_service)
    text_updater = cast(Any, updater.text_updater)
    logger = cast(Any, updater.logger)

    documento = Mock()

    word_service.abrir_documento.return_value = documento

    erro = RuntimeError(
        "Erro durante atualização do ano."
    )

    text_updater.atualizar_ano.side_effect = erro

    with pytest.raises(
        RuntimeError,
        match="Erro durante atualização do ano.",
    ):
        updater.atualizar_ano(
            arquivo=arquivo,
            ano_origem=2026,
            ano_destino=2027,
            destino=destino,
        )

    logger.exception.assert_called_once()