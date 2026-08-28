"""
Agenda Universal PRO
Arquivo: config/agenda_config.py

Configuração específica para uma execução de atualização
de uma agenda.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgendaConfig:
    """Representa a configuração de uma execução da agenda."""

    arquivo_origem: Path
    arquivo_destino: Path
    ano_origem: int
    ano_destino: int

    def __post_init__(self) -> None:
        """Normaliza os caminhos da configuração."""

        object.__setattr__(
            self,
            "arquivo_origem",
            Path(self.arquivo_origem),
        )

        object.__setattr__(
            self,
            "arquivo_destino",
            Path(self.arquivo_destino),
        )

    @property
    def nome_arquivo_origem(self) -> str:
        """Retorna o nome do arquivo de origem."""

        return self.arquivo_origem.name

    @property
    def nome_arquivo_destino(self) -> str:
        """Retorna o nome do arquivo de destino."""

        return self.arquivo_destino.name