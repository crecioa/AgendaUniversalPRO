from __future__ import annotations

import re
from datetime import datetime


class DateParser:
    """Utilitário para localizar e manipular datas."""

    DATE_PATTERN = re.compile(
        r"\b(0?[1-9]|[12][0-9]|3[01])/"
        r"(0?[1-9]|1[0-2])/"
        r"(\d{4})\b"
    )

    DIAS_SEMANA = (
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
        "Domingo",
    )

    @classmethod
    def encontrar_datas(cls, texto: str) -> list[str]:
        """Localiza datas no formato dd/mm/aaaa."""
        return [
            match.group(0)
            for match in cls.DATE_PATTERN.finditer(texto)
        ]

    @staticmethod
    def validar_data(data: str) -> bool:
        """Verifica se uma data é válida."""
        try:
            datetime.strptime(data, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def converter_data(data: str) -> datetime | None:
        """Converte uma data textual em datetime."""
        try:
            return datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            return None

    @staticmethod
    def atualizar_ano(
        data: str,
        novo_ano: int,
    ) -> str | None:
        """Atualiza o ano de uma data válida."""
        data_convertida = DateParser.converter_data(data)

        if data_convertida is None:
            return None

        try:
            nova_data = data_convertida.replace(year=novo_ano)
        except ValueError:
            return None

        return nova_data.strftime("%d/%m/%Y")

    @staticmethod
    def obter_dia_semana(data: str) -> str | None:
        """Retorna o dia da semana de uma data no formato dd/mm/aaaa."""
        data_convertida = DateParser.converter_data(data)

        if data_convertida is None:
            return None

        return DateParser.DIAS_SEMANA[data_convertida.weekday()]
