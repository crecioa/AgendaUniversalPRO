
"""
Agenda Universal PRO
Arquivo: config/settings.py

Configurações globais e diretórios da aplicação.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


APP_NAME = "Agenda Universal PRO"
APP_VERSION = "1.1.1"
APP_AUTHOR = "Crecio Santos"


def obter_diretorio_base() -> Path:
    """Define o diretório de dados da aplicação."""

    if getattr(sys, "frozen", False):
        local_appdata = os.environ.get("LOCALAPPDATA")

        if local_appdata:
            return Path(local_appdata) / "AgendaUniversalPRO"

        return (
            Path.home()
            / "AppData"
            / "Local"
            / "AgendaUniversalPRO"
        )

    return Path(__file__).resolve().parent.parent


BASE_DIR = obter_diretorio_base()

CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"
BACKUP_DIR = BASE_DIR / "backup"
OUTPUT_DIR = BASE_DIR / "output"
MODELOS_DIR = BASE_DIR / "modelos"

LOG_FILE = LOGS_DIR / "agenda_universal.log"

SUPPORTED_EXTENSIONS = (".doc", ".docx")
OUTPUT_SUFFIX = "_REVISADO"
BACKUP_PREFIX = "BACKUP_"
LOG_LEVEL = "INFO"


def create_directories() -> None:
    """Cria os diretórios necessários."""

    for directory in (
        LOGS_DIR,
        BACKUP_DIR,
        OUTPUT_DIR,
        MODELOS_DIR,
    ):
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )
