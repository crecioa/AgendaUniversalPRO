"""
Agenda Universal PRO
Arquivo: core/calendar_service.py

Serviço responsável por operações de calendário.
"""

from __future__ import annotations

from datetime import date

from core.holiday_service import HolidayService


class CalendarService:
    """Serviço para consulta de informações do calendário."""

    DIAS_SEMANA = (
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    )

    @staticmethod
    def dia_semana(data: date) -> str:
        """Retorna o nome do dia da semana."""

        return CalendarService.DIAS_SEMANA[data.weekday()]

    @staticmethod
    def fim_de_semana(data: date) -> bool:
        """Verifica se é sábado ou domingo."""

        return data.weekday() >= 5

    @staticmethod
    def eh_feriado(data: date) -> bool:
        """Verifica se é feriado."""

        return HolidayService.eh_feriado(data)

    @staticmethod
    def nome_feriado(data: date) -> str | None:
        """Retorna o nome do feriado."""

        return HolidayService.nome_feriado(data)

    @classmethod
    def resumo_data(cls, data: date) -> dict:
        """Retorna um resumo das informações da data."""

        return {
            "data": data.strftime("%d/%m/%Y"),
            "dia_semana": cls.dia_semana(data),
            "fim_de_semana": cls.fim_de_semana(data),
            "feriado": cls.eh_feriado(data),
            "nome_feriado": cls.nome_feriado(data),
        }