"""
Agenda Universal PRO
Arquivo: tests/test_backup_service.py

Testes do BackupService.

Sprint 4.8:
- Valida criação de backup.
- Valida preservação do conteúdo original.
- Valida nome e extensão do backup.
- Valida tratamento de arquivo inexistente.
- Valida registro da criação do backup.
"""

from pathlib import Path
from typing import Any, cast
from unittest.mock import Mock

import pytest

import services.backup_service as backup_module
from services.backup_service import BackupService


def test_criar_backup_copia_arquivo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Valida a criação de uma cópia do arquivo."""

    pasta_backup = tmp_path / "backup"

    monkeypatch.setattr(
        backup_module,
        "BACKUP_DIR",
        pasta_backup,
    )

    arquivo = tmp_path / "agenda.docx"

    conteudo = "Conteúdo original da agenda."

    arquivo.write_text(
        conteudo,
        encoding="utf-8",
    )

    resultado = BackupService.criar_backup(
        arquivo
    )

    assert resultado.exists()
    assert resultado.is_file()

    assert resultado.parent == pasta_backup

    assert resultado.name.startswith(
        "agenda_"
    )

    assert resultado.suffix == ".docx"

    assert resultado.read_text(
        encoding="utf-8"
    ) == conteudo

    assert arquivo.read_text(
        encoding="utf-8"
    ) == conteudo


def test_criar_backup_registra_log(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Valida o registro da criação do backup."""

    pasta_backup = tmp_path / "backup"

    monkeypatch.setattr(
        backup_module,
        "BACKUP_DIR",
        pasta_backup,
    )

    logger = Mock()

    monkeypatch.setattr(
        backup_module.LoggerService,
        "get_logger",
        lambda: logger,
    )

    arquivo = tmp_path / "agenda.docx"

    arquivo.write_text(
        "Conteúdo para backup.",
        encoding="utf-8",
    )

    resultado = BackupService.criar_backup(
        arquivo
    )

    logger.info.assert_called_once()

    mensagem = cast(
        Any,
        logger.info.call_args,
    ).args[0]

    assert "Backup criado:" in mensagem
    assert resultado.name in mensagem


def test_criar_backup_arquivo_inexistente(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Valida erro quando o arquivo original não existe."""

    pasta_backup = tmp_path / "backup"

    monkeypatch.setattr(
        backup_module,
        "BACKUP_DIR",
        pasta_backup,
    )

    arquivo = tmp_path / "nao_existe.docx"

    with pytest.raises(
        FileNotFoundError,
        match="Arquivo não encontrado",
    ):
        BackupService.criar_backup(
            arquivo
        )

    assert not pasta_backup.exists()