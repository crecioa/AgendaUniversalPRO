
"""
Agenda Universal PRO
Arquivo: services/config_service.py

Gerencia o carregamento e o salvamento das configurações
persistentes da aplicação.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any
from config.settings import MODELOS_DIR, OUTPUT_DIR
from config.app_config import AppConfig


class ConfigService:
    """Gerencia as configurações persistentes da aplicação."""

    DIRETORIO_ORIGEM_PADRAO = MODELOS_DIR
    DIRETORIO_DESTINO_PADRAO = OUTPUT_DIR

    def __init__(
        self,
        arquivo_config: Path | None = None,
    ) -> None:
        if arquivo_config is None:
            arquivo_config = self._caminho_configuracao_padrao()

        self.arquivo_config = Path(arquivo_config)

    @staticmethod
    def _caminho_configuracao_padrao() -> Path:
        """Define onde salvar as configurações."""

        if getattr(sys, "frozen", False):
            local_appdata = os.environ.get("LOCALAPPDATA")

            if local_appdata:
                base = Path(local_appdata)
            else:
                base = Path.home() / "AppData" / "Local"

            return (
                base
                / "AgendaUniversalPRO"
                / "app_config.json"
            )

        return Path("data") / "app_config.json"

    def carregar(self) -> AppConfig:
        """Carrega as configurações persistentes."""

        if not self.arquivo_config.exists():
            return self._configuracao_padrao()

        try:
            with self.arquivo_config.open(
                "r",
                encoding="utf-8",
            ) as arquivo:
                dados: Any = json.load(arquivo)

            if not isinstance(dados, dict):
                return self._configuracao_padrao()

            diretorio_origem = self._obter_diretorio(
                dados.get("diretorio_origem"),
                self.DIRETORIO_ORIGEM_PADRAO,
            )

            diretorio_destino = self._obter_diretorio(
                dados.get("diretorio_destino"),
                self.DIRETORIO_DESTINO_PADRAO,
            )

            return AppConfig(
                diretorio_origem=diretorio_origem,
                diretorio_destino=diretorio_destino,
            )

        except (json.JSONDecodeError, OSError):
            return self._configuracao_padrao()

    def salvar(self, config: AppConfig) -> None:
        """Salva as configurações persistentemente."""

        self.arquivo_config.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dados = {
            "diretorio_origem": str(config.diretorio_origem),
            "diretorio_destino": str(config.diretorio_destino),
        }

        with self.arquivo_config.open(
            "w",
            encoding="utf-8",
        ) as arquivo:
            json.dump(
                dados,
                arquivo,
                ensure_ascii=False,
                indent=4,
            )

    @classmethod
    def _configuracao_padrao(cls) -> AppConfig:
        """Retorna uma configuração padrão segura."""

        return AppConfig(
            diretorio_origem=cls.DIRETORIO_ORIGEM_PADRAO,
            diretorio_destino=cls.DIRETORIO_DESTINO_PADRAO,
        )

    @staticmethod
    def _obter_diretorio(
        valor: Any,
        valor_padrao: Path,
    ) -> Path:
        """Converte um valor válido em Path."""

        if not isinstance(valor, str):
            return valor_padrao

        valor_limpo = valor.strip()

        if not valor_limpo:
            return valor_padrao

        return Path(valor_limpo)
