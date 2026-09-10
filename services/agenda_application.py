"""
Agenda Universal PRO
Arquivo: services/agenda_application.py

Camada de aplicação responsável por coordenar os fluxos
de atualização de agendas.

Sprint 4.5:
- Registra erros ocorridos durante as operações.
- Preserva a exceção original para tratamento pela camada superior.
"""

from __future__ import annotations

from pathlib import Path

from config.agenda_config import AgendaConfig
from core.agenda_updater import AgendaUpdater
from services.logger_service import LoggerService


class AgendaApplication:
    """Coordena os principais fluxos de atualização da agenda."""

    def __init__(self) -> None:
        """Inicializa a camada de aplicação."""

        self.logger = LoggerService.get_logger()
        self.agenda_updater = AgendaUpdater()

    def atualizar_ano(
        self,
        arquivo: str | Path,
        ano_origem: int,
        ano_destino: int,
        destino: str | Path,
    ) -> int:
        """
        Atualiza automaticamente o ano das datas de uma agenda.

        Args:
            arquivo: Documento Word original.
            ano_origem: Ano atual das datas.
            ano_destino: Novo ano das datas.
            destino: Caminho do documento atualizado.

        Returns:
            Quantidade de datas atualizadas.
        """

        self.logger.info(
            "Aplicação: iniciando atualização de ano."
        )

        try:
            quantidade = self.agenda_updater.atualizar_ano(
                arquivo=arquivo,
                ano_origem=ano_origem,
                ano_destino=ano_destino,
                destino=destino,
            )

            self.logger.info(
                "Aplicação: atualização concluída. "
                "%d substituição(ões) realizada(s).",
                quantidade,
            )

            return quantidade

        except Exception:
            self.logger.exception(
                "Aplicação: erro durante atualização de ano. "
                "Origem: %s | Destino: %s",
                arquivo,
                destino,
            )
            raise

    def atualizar_datas(
        self,
        arquivo: str | Path,
        substituicoes: dict[str, str],
        destino: str | Path,
    ) -> int:
        """
        Atualiza datas específicas de uma agenda.

        Args:
            arquivo: Documento Word original.
            substituicoes: Dicionário no formato
                {"data_antiga": "data_nova"}.
            destino: Caminho do documento atualizado.

        Returns:
            Quantidade de substituições realizadas.
        """

        self.logger.info(
            "Aplicação: iniciando atualização de datas."
        )

        try:
            quantidade = self.agenda_updater.atualizar_agenda(
                arquivo=arquivo,
                substituicoes=substituicoes,
                destino=destino,
            )

            self.logger.info(
                "Aplicação: atualização concluída. "
                "%d substituição(ões) realizada(s).",
                quantidade,
            )

            return quantidade

        except Exception:
            self.logger.exception(
                "Aplicação: erro durante atualização de datas. "
                "Origem: %s | Destino: %s",
                arquivo,
                destino,
            )
            raise

    def atualizar(
        self,
        config: AgendaConfig,
    ) -> int:
        """
        Atualiza uma agenda utilizando uma configuração.

        Args:
            config: Configuração da atualização da agenda.

        Returns:
            Quantidade de datas atualizadas.
        """

        self.logger.info(
            "Aplicação: iniciando atualização "
            "utilizando configuração."
        )

        try:
            quantidade = self.atualizar_ano(
                arquivo=config.arquivo_origem,
                ano_origem=config.ano_origem,
                ano_destino=config.ano_destino,
                destino=config.arquivo_destino,
            )

            self.logger.info(
                "Aplicação: atualização por configuração "
                "concluída. %d substituição(ões) realizada(s).",
                quantidade,
            )

            return quantidade

        except Exception:
            self.logger.exception(
                "Aplicação: erro durante atualização "
                "utilizando configuração."
            )
            raise