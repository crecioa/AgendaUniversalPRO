"""
Agenda Universal PRO
Arquivo: config/app_config.py

Modelo de configuração persistente da aplicação.

Sprint 4.1:

* Configurações persistentes.
  """

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass
class AppConfig:
  """Representa as configurações persistentes da aplicação."""

  diretorio_origem: Path = Path("modelos")
  diretorio_destino: Path = Path("output")
