"""
Agenda Universal PRO
Arquivo: core/date_parser.py

Responsável por identificar e validar datas em textos.
"""

from __future__ import annotations

import re
from datetime import datetime


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
    def converter_data(data: str) -> datetime | None:
        """
        Converte uma string em datetime.
        """

        try:
            return datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            return None

    @staticmethod
    def atualizar_ano(data: str, novo_ano: int) -> str | None:
        """
        Atualiza o ano de uma data.

        Args:
            data: Data no formato dd/mm/aaaa.
            novo_ano: Ano que deverá substituir o ano atual.

        Returns:
            Data com o novo ano ou None se a nova data for inválida.
        """

        data_convertida = DateParser.converter_data(data)

        if data_convertida is None:
            return None

        try:
            nova_data = data_convertida.replace(year=novo_ano)
        except ValueError:
            return None

        return nova_data.strftime("%d/%m/%Y")