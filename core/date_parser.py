"""
Agenda Universal PRO
Arquivo: core/date_parser.py

Responsável por identificar e validar datas em textos.
"""

from __future__ import annotations

import re
from datetime import datetime
from typing import Optional


class DateParser:
    """Utilitário para localizar e validar datas."""

    # Formato: dd/mm/aaaa
    DATE_PATTERN = re.compile(
        r"\b(0?[1-9]|[12][0-9]|3[01])/"
        r"(0?[1-9]|1[0-2])/"
        r"(\d{4})\b"
    )

    @classmethod
    def encontrar_datas(cls, texto: str) -> list[str]:
        """
        Retorna todas as datas encontradas no texto.
        """

        return [
            match.group(0)
            for match in cls.DATE_PATTERN.finditer(texto)
        ]

    @staticmethod
    def validar_data(data: str) -> bool:
        """
        Verifica se a data é válida.
        """

        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def converter_data(data: str) -> Optional[datetime]:
        """
        Converte uma string em datetime.
        """

        try:
            return datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            return None