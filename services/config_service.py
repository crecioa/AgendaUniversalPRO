"""ServiÃ§o de configuraÃ§Ã£o da Agenda Universal PRO.

ResponsÃ¡vel pelo carregamento e salvamento das configuraÃ§Ãµes persistentes
da aplicaÃ§Ã£o.

Sprint 4.1: persistÃªncia de configuraÃ§Ãµes em JSON.
"""

from __future__ import annotations

import json
from pathlib import Path

from config.app_config import AppConfig

class ConfigService:
    """Gerencia as configuraÃ§Ãµes persistentes da aplicaÃ§Ã£o."""

    def __init__(
        self,
        arquivo_config: Path | None = None,
    ) -> None:
        if arquivo_config is None:
            arquivo_config = (
                Path("data") / "app_config.json"
            )

        self.arquivo_config = arquivo_config

    def carregar(self) -> AppConfig:
        """Carrega as configuraÃ§Ãµes persistentes."""

        if not self.arquivo_config.exists():
            return AppConfig()

        try:
            with self.arquivo_config.open(
                "r",
                encoding="utf-8",
            ) as arquivo:
                dados = json.load(arquivo)

            return AppConfig(
                diretorio_origem=Path(
                    dados.get(
                        "diretorio_origem",
                        "modelos",
                    )
                ),
                diretorio_destino=Path(
                    dados.get(
                        "diretorio_destino",
                        "output",
                    )
                ),
            )

        except (
            json.JSONDecodeError,
            OSError,
        ):
            return AppConfig()

    def salvar(
        self,
        config: AppConfig,
    ) -> None:
        """Salva as configuraÃ§Ãµes persistentemente."""

        self.arquivo_config.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dados = {
            "diretorio_origem": str(
                config.diretorio_origem
            ),
            "diretorio_destino": str(
                config.diretorio_destino
            ),
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


