"""
Agenda Universal PRO
Arquivo: core/holiday_service.py

Serviço para consulta de feriados nacionais.
"""

from __future__ import annotations

from datetime import date


class HolidayService:
    """Gerencia os feriados nacionais fixos."""

    FERIADOS_FIXOS = {
        (1, 1): "Confraternização Universal",
        (4, 21): "Tiradentes",
        (5, 1): "Dia do Trabalhador",
        (9, 7): "Independência do Brasil",
        (10, 12): "Nossa Senhora Aparecida",
        (11, 2): "Finados",
        (11, 15): "Proclamação da República",
        (12, 25): "Natal",
    }

    @classmethod
    def nome_feriado(cls, data: date) -> str | None:
        """Retorna o nome do feriado, se existir."""

        return cls.FERIADOS_FIXOS.get((data.month, data.day))

    @classmethod
    def eh_feriado(cls, data: date) -> bool:
        """Verifica se a data é um feriado fixo."""

        return (data.month, data.day) in cls.FERIADOS_FIXOS