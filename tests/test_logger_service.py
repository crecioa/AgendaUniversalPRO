
"""
Agenda Universal PRO
Arquivo: tests/test_logger_service.py

Testes do serviço centralizado de logging.

Sprint 4.10:
- Testa criação do logger.
- Testa comportamento Singleton.
- Testa configuração dos handlers.
- Testa gravação em arquivo.
- Testa mensagens iniciais.
"""

import logging
from pathlib import Path
from typing import Any

import services.logger_service as logger_module
from services.logger_service import LoggerService


def limpar_logger() -> None:
    """Remove handlers e reseta o logger usado nos testes."""

    logger = logging.getLogger("AgendaUniversal")

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    LoggerService._logger = None


def test_get_logger_cria_logger(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa a criação inicial do logger."""

    arquivo_log = tmp_path / "agenda.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        arquivo_log,
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_LEVEL",
        "INFO",
    )

    monkeypatch.setattr(
        logger_module,
        "create_directories",
        lambda: None,
    )

    limpar_logger()

    logger = LoggerService.get_logger()

    assert logger.name == "AgendaUniversal"
    assert logger.level == logging.INFO
    assert len(logger.handlers) == 2

    limpar_logger()


def test_get_logger_retorna_mesma_instancia(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa o comportamento Singleton do LoggerService."""

    arquivo_log = tmp_path / "agenda.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        arquivo_log,
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_LEVEL",
        "INFO",
    )

    monkeypatch.setattr(
        logger_module,
        "create_directories",
        lambda: None,
    )

    limpar_logger()

    primeiro_logger = LoggerService.get_logger()
    segundo_logger = LoggerService.get_logger()

    assert primeiro_logger is segundo_logger

    limpar_logger()


def test_get_logger_configura_handlers(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa a configuração dos handlers."""

    arquivo_log = tmp_path / "agenda.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        arquivo_log,
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_LEVEL",
        "DEBUG",
    )

    monkeypatch.setattr(
        logger_module,
        "create_directories",
        lambda: None,
    )

    limpar_logger()

    logger = LoggerService.get_logger()

    assert len(logger.handlers) == 2

    tipos_handlers = {
        type(handler)
        for handler in logger.handlers
    }

    assert logging.FileHandler in tipos_handlers
    assert logging.StreamHandler in tipos_handlers

    limpar_logger()


def test_get_logger_grava_em_arquivo(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa a gravação de mensagens no arquivo de log."""

    arquivo_log = tmp_path / "agenda.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        arquivo_log,
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_LEVEL",
        "INFO",
    )

    monkeypatch.setattr(
        logger_module,
        "create_directories",
        lambda: None,
    )

    limpar_logger()

    logger = LoggerService.get_logger()

    logger.info("Mensagem de teste da Sprint 4.10.")

    for handler in logger.handlers:
        handler.flush()

    assert arquivo_log.exists()

    conteudo = arquivo_log.read_text(
        encoding="utf-8",
    )

    assert "Agenda Universal PRO iniciado." in conteudo
    assert "Mensagem de teste da Sprint 4.10." in conteudo

    limpar_logger()


def test_get_logger_registra_mensagens_iniciais(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa as mensagens registradas na inicialização."""

    arquivo_log = tmp_path / "agenda.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        arquivo_log,
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_LEVEL",
        "INFO",
    )

    monkeypatch.setattr(
        logger_module,
        "create_directories",
        lambda: None,
    )

    limpar_logger()

    LoggerService.get_logger()

    conteudo = arquivo_log.read_text(
        encoding="utf-8",
    )

    assert "=" * 60 in conteudo
    assert "Agenda Universal PRO iniciado." in conteudo

    limpar_logger()


def test_get_logger_reutiliza_logger_com_handlers(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa reutilização quando o logger já possui handlers."""

    arquivo_log = tmp_path / "agenda.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        arquivo_log,
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_LEVEL",
        "INFO",
    )

    monkeypatch.setattr(
        logger_module,
        "create_directories",
        lambda: None,
    )

    limpar_logger()

    logger = logging.getLogger("AgendaUniversal")

    handler = logging.StreamHandler()
    logger.addHandler(handler)

    LoggerService._logger = None

    resultado = LoggerService.get_logger()

    assert resultado is logger
    assert LoggerService._logger is logger
    assert len(logger.handlers) == 1

    handler.close()
    logger.removeHandler(handler)
    LoggerService._logger = None


def test_get_logger_usa_nivel_configurado(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa o nível configurado para o logger."""

    arquivo_log = tmp_path / "agenda.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        arquivo_log,
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_LEVEL",
        "WARNING",
    )

    monkeypatch.setattr(
        logger_module,
        "create_directories",
        lambda: None,
    )

    limpar_logger()

    logger = LoggerService.get_logger()

    assert logger.level == logging.WARNING

    limpar_logger()


def test_logger_service_expoe_logger_tipado(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    """Testa que o logger retornado possui a interface esperada."""

    arquivo_log = tmp_path / "agenda.log"

    monkeypatch.setattr(
        logger_module,
        "LOG_FILE",
        arquivo_log,
    )

    monkeypatch.setattr(
        logger_module,
        "LOG_LEVEL",
        "INFO",
    )

    monkeypatch.setattr(
        logger_module,
        "create_directories",
        lambda: None,
    )

    limpar_logger()

    logger = LoggerService.get_logger()

    assert isinstance(
        logger,
        logging.Logger,
    )

    assert hasattr(logger, "info")
    assert hasattr(logger, "error")
    assert hasattr(logger, "exception")

    limpar_logger()