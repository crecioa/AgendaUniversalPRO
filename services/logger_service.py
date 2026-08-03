"""
Agenda Universal PRO
Arquivo: services/logger_service.py

Serviço centralizado de logging da aplicação.
"""

from __future__ import annotations

from __future__ import annotations

import logging
from logging import Logger
from pathlib import Path

from config.settings import LOG_FILE, LOG_LEVEL, create_directories


class LoggerService:
    """Responsável por configurar e fornecer o logger da aplicação."""

    _logger: Logger | None = None

    @classmethod
    def get_logger(cls) -> Logger:
        """
        Retorna uma instância única (Singleton) do logger.
        """

        if cls._logger is not None:
            return cls._logger

        create_directories()

        logger = logging.getLogger("AgendaUniversal")
        logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))

        if logger.handlers:
            cls._logger = logger
            return logger

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s",
            datefmt="%d/%m/%Y %H:%M:%S",
        )

        # Log em arquivo
        file_handler = logging.FileHandler(
            Path(LOG_FILE),
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        # Log no console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        cls._logger = logger

        logger.info("=" * 60)
        logger.info("Agenda Universal PRO iniciado.")
        logger.info("=" * 60)

        return logger