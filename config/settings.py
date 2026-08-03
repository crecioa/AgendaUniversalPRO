"""
Agenda Universal PRO
Arquivo: config/settings.py

Configurações globais da aplicação.
"""

from pathlib import Path

# ==========================================================
# Diretórios do Projeto
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR = BASE_DIR / "logs"
BACKUP_DIR = BASE_DIR / "backup"
OUTPUT_DIR = BASE_DIR / "output"
MODELOS_DIR = BASE_DIR / "modelos"

# ==========================================================
# Arquivos
# ==========================================================

LOG_FILE = LOGS_DIR / "agenda_universal.log"

# ==========================================================
# Aplicação
# ==========================================================

APP_NAME = "Agenda Universal PRO"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Crecio Santos"

# ==========================================================
# Word
# ==========================================================

SUPPORTED_EXTENSIONS = (".doc", ".docx")

OUTPUT_SUFFIX = "_REVISADO"

# ==========================================================
# Backup
# ==========================================================

BACKUP_PREFIX = "BACKUP_"

# ==========================================================
# Logging
# ==========================================================

LOG_LEVEL = "INFO"

# ==========================================================
# Inicialização
# ==========================================================

def create_directories() -> None:
    """
    Cria automaticamente todas as pastas necessárias.
    """

    for directory in (
        LOGS_DIR,
        BACKUP_DIR,
        OUTPUT_DIR,
        MODELOS_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)