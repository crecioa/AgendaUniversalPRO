"""
Agenda Universal PRO
Arquivo: services/agenda_application.py

Camada de aplicação responsável por coordenar os fluxos
de atualização de agendas.
"""

from __future__ import annotations

from pathlib import Path

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
        """Atualiza automaticamente o ano das datas de uma agenda."""

        self.logger.info(
            "Aplicação: iniciando atualização de ano."
        )

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

    def atualizar_datas(
        self,
        arquivo: str | Path,
        substituicoes: dict[str, str],
        destino: str | Path,
    ) -> int:
        """Atualiza datas específicas de uma agenda."""

        self.logger.info(
            "Aplicação: iniciando atualização de datas."
        )

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
