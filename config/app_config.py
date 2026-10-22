
"""
Agenda Universal PRO
Arquivo: config/app_config.py

Modelo de configuração persistente da aplicação.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from config.settings import MODELOS_DIR, OUTPUT_DIR


@dataclass
class AppConfig:
    """Representa as configurações persistentes da aplicação."""

    diretorio_origem: Path = field(
        default_factory=lambda: MODELOS_DIR
    )

    diretorio_destino: Path = field(
        default_factory=lambda: OUTPUT_DIR
    )
