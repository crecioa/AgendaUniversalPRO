
"""
Agenda Universal PRO
Arquivo: services/text_updater.py

Serviço responsável por localizar e atualizar datas e dias da semana
nos parágrafos e tabelas de um documento Word.
"""

from __future__ import annotations

import re
from logging import Logger
from typing import Callable

from docx.document import Document as DocxDocument
from docx.table import _Cell

from core.date_parser import DateParser
from services.logger_service import LoggerService


class TextUpdater:
    """Localiza e atualiza datas em documentos Word."""

    DIAS_SEMANA_PATTERN = (
        r"Segunda-feira|Terça-feira|Quarta-feira|"
        r"Quinta-feira|Sexta-feira|Sábado|Domingo"
    )

    DATA_COM_DIA_PATTERN = re.compile(
        rf"(?P<dia>{DIAS_SEMANA_PATTERN})"
        r"(?P<separador>\s*[,–—-]\s*)"
        r"(?P<data>\d{1,2}/\d{1,2}/\d{4})",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        self.logger: Logger = LoggerService.get_logger()

    def localizar_datas(
        self,
        documento: DocxDocument,
    ) -> list[tuple[int, str, list[str]]]:
        """
        Percorre os parágrafos procurando datas.

        Returns:
            Lista contendo:
                (índice do parágrafo, texto, datas encontradas)
        """

        ocorrencias: list[tuple[int, str, list[str]]] = []

        self.logger.info(
            "Iniciando leitura dos parágrafos."
        )

        for indice, paragrafo in enumerate(
            documento.paragraphs
        ):
            texto = paragrafo.text.strip()

            if not texto:
                continue

            datas = DateParser.encontrar_datas(texto)

            if datas:
                ocorrencias.append(
                    (indice, texto, datas)
                )

                self.logger.info(
                    "Parágrafo %s: %d data(s) encontrada(s): %s",
                    indice,
                    len(datas),
                    ", ".join(datas),
                )

        self.logger.info(
            "Leitura concluída. %d parágrafo(s) com datas.",
            len(ocorrencias),
        )

        return ocorrencias

    @staticmethod
    def _substituir_texto(
        texto: str,
        substituicoes: dict[str, str],
    ) -> tuple[str, int]:
        """
        Substitui datas em um texto.

        Returns:
            Tupla contendo:
                (texto atualizado, quantidade de substituições)
        """

        texto_atualizado = texto
        quantidade = 0

        for data_antiga, data_nova in substituicoes.items():
            ocorrencias = texto_atualizado.count(
                data_antiga
            )

            if ocorrencias:
                texto_atualizado = texto_atualizado.replace(
                    data_antiga,
                    data_nova,
                )

                quantidade += ocorrencias

        return texto_atualizado, quantidade

    def _atualizar_paragrafo(
        self,
        paragrafo,
        substituicoes: dict[str, str],
    ) -> int:
        """Atualiza as substituições de um parágrafo."""

        texto_original = paragrafo.text

        if not texto_original.strip():
            return 0

        texto_atualizado, quantidade = (
            self._substituir_texto(
                texto_original,
                substituicoes,
            )
        )

        if texto_atualizado != texto_original:
            paragrafo.text = texto_atualizado

        return quantidade

    def _atualizar_celula(
        self,
        celula: _Cell,
        substituicoes: dict[str, str],
    ) -> int:
        """
        Atualiza as substituições nos parágrafos de uma célula.
        """

        quantidade = 0

        for paragrafo in celula.paragraphs:
            quantidade += self._atualizar_paragrafo(
                paragrafo,
                substituicoes,
            )

        return quantidade

    def atualizar_datas(
        self,
        documento: DocxDocument,
        substituicoes: dict[str, str],
    ) -> int:
        """
        Substitui datas nos parágrafos e tabelas do documento.

        Returns:
            Quantidade de substituições realizadas.
        """

        quantidade = 0

        self.logger.info(
            "Iniciando atualização das datas."
        )

        for paragrafo in documento.paragraphs:
            quantidade += self._atualizar_paragrafo(
                paragrafo,
                substituicoes,
            )

        for tabela in documento.tables:
            for linha in tabela.rows:
                for celula in linha.cells:
                    quantidade += self._atualizar_celula(
                        celula,
                        substituicoes,
                    )

        self.logger.info(
            "Atualização concluída. "
            "%d substituição(ões) realizada(s).",
            quantidade,
        )

        return quantidade

    @staticmethod
    def _atualizar_dia_e_data(
        texto: str,
        ano_origem: int,
        ano_destino: int,
    ) -> tuple[str, int, set[str]]:
        """
        Atualiza pares de dia da semana e data.

        Returns:
            Tupla contendo:
                (texto atualizado, quantidade, datas processadas)
        """

        quantidade = 0
        datas_processadas: set[str] = set()

        def substituir_par(
            match: re.Match[str],
        ) -> str:
            nonlocal quantidade

            data_antiga = match.group("data")
            data_convertida = DateParser.converter_data(
                data_antiga
            )

            if data_convertida is None:
                return match.group(0)

            if data_convertida.year != ano_origem:
                return match.group(0)

            nova_data = DateParser.atualizar_ano(
                data_antiga,
                ano_destino,
            )

            if nova_data is None:
                return match.group(0)

            novo_dia = DateParser.obter_dia_semana(
                nova_data
            )

            if novo_dia is None:
                return match.group(0)

            quantidade += 1
            datas_processadas.add(data_antiga)

            return (
                f"{novo_dia}"
                f"{match.group('separador')}"
                f"{nova_data}"
            )

        texto_atualizado = TextUpdater.DATA_COM_DIA_PATTERN.sub(
            substituir_par,
            texto,
        )

        return (
            texto_atualizado,
            quantidade,
            datas_processadas,
        )

    @staticmethod
    def _atualizar_datas_restantes(
        texto: str,
        ano_origem: int,
        ano_destino: int,
        datas_processadas: set[str],
    ) -> tuple[str, int]:
        """
        Atualiza datas que não possuem o dia da semana associado.
        """

        quantidade = 0
        texto_atualizado = texto

        datas = DateParser.encontrar_datas(texto)

        for data in datas:
            if data in datas_processadas:
                continue

            data_convertida = DateParser.converter_data(data)

            if data_convertida is None:
                continue

            if data_convertida.year != ano_origem:
                continue

            nova_data = DateParser.atualizar_ano(
                data,
                ano_destino,
            )

            if nova_data is None:
                continue

            ocorrencias = texto_atualizado.count(data)

            if ocorrencias:
                texto_atualizado = texto_atualizado.replace(
                    data,
                    nova_data,
                )

                quantidade += ocorrencias

        return texto_atualizado, quantidade

    def atualizar_ano(
        self,
        documento: DocxDocument,
        ano_origem: int,
        ano_destino: int,
    ) -> int:
        """
        Atualiza automaticamente o ano das datas existentes
        nos parágrafos e tabelas do documento.

        Também recalcula o dia da semana quando ele aparece
        associado à data.

        Returns:
            Quantidade de datas atualizadas.
        """

        quantidade = 0

        self.logger.info(
            "Iniciando atualização automática de %d para %d.",
            ano_origem,
            ano_destino,
        )

        def atualizar_texto(
            texto: str,
        ) -> tuple[str, int]:
            texto_atualizado, quantidade_dias, datas_processadas = (
                self._atualizar_dia_e_data(
                    texto,
                    ano_origem,
                    ano_destino,
                )
            )

            texto_atualizado, quantidade_restante = (
                self._atualizar_datas_restantes(
                    texto_atualizado,
                    ano_origem,
                    ano_destino,
                    datas_processadas,
                )
            )

            return (
                texto_atualizado,
                quantidade_dias + quantidade_restante,
            )

        def atualizar_paragrafo(paragrafo) -> int:
            texto_original = paragrafo.text

            if not texto_original.strip():
                return 0

            texto_atualizado, quantidade_local = (
                atualizar_texto(texto_original)
            )

            if texto_atualizado != texto_original:
                paragrafo.text = texto_atualizado

            return quantidade_local

        for paragrafo in documento.paragraphs:
            quantidade += atualizar_paragrafo(
                paragrafo
            )

        for tabela in documento.tables:
            for linha in tabela.rows:
                for celula in linha.cells:
                    for paragrafo in celula.paragraphs:
                        quantidade += atualizar_paragrafo(
                            paragrafo
                        )

        self.logger.info(
            "Atualização automática concluída. "
            "%d substituição(ões) realizada(s).",
            quantidade,
        )

        return quantidade