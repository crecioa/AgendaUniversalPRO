"""
Agenda Universal PRO
Arquivo: services/text_updater.py

Serviço responsável por localizar e atualizar datas
nos parágrafos e tabelas de um documento Word.
"""

from __future__ import annotations

from logging import Logger

from docx.document import Document as DocxDocument
from docx.table import _Cell

from core.date_parser import DateParser
from services.logger_service import LoggerService


class TextUpdater:
    """Localiza e atualiza datas em documentos Word."""

    def __init__(self) -> None:
        self.logger: Logger = LoggerService.get_logger()

    def localizar_datas(
        self,
        documento: DocxDocument,
    ) -> list[tuple[int, str, list[str]]]:
        """
        Percorre os parágrafos procurando datas.

        Args:
            documento: Documento Word aberto.

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

        Args:
            documento: Documento Word aberto.
            substituicoes: Dicionário no formato:
                {"data_antiga": "data_nova"}

        Returns:
            Quantidade de substituições realizadas.
        """

        quantidade = 0

        self.logger.info(
            "Iniciando atualização das datas."
        )

        # Atualiza parágrafos normais.
        for paragrafo in documento.paragraphs:
            quantidade += self._atualizar_paragrafo(
                paragrafo,
                substituicoes,
            )

        # Atualiza células das tabelas.
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

    def atualizar_ano(
        self,
        documento: DocxDocument,
        ano_origem: int,
        ano_destino: int,
    ) -> int:
        """
        Atualiza automaticamente o ano das datas existentes
        nos parágrafos e tabelas do documento.

        Args:
            documento: Documento Word aberto.
            ano_origem: Ano das datas que serão atualizadas.
            ano_destino: Novo ano das datas.

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
            """Atualiza as datas encontradas em um texto."""

            texto_atualizado = texto
            quantidade_local = 0

            datas = DateParser.encontrar_datas(texto)

            for data in datas:
                data_convertida = (
                    DateParser.converter_data(data)
                )

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
                    texto_atualizado = (
                        texto_atualizado.replace(
                            data,
                            nova_data,
                        )
                    )

                    quantidade_local += ocorrencias

            return texto_atualizado, quantidade_local

        # -----------------------------------------------------
        # PARÁGRAFOS
        # -----------------------------------------------------

        for paragrafo in documento.paragraphs:
            texto_original = paragrafo.text

            if not texto_original.strip():
                continue

            texto_atualizado, quantidade_local = (
                atualizar_texto(texto_original)
            )

            if texto_atualizado != texto_original:
                paragrafo.text = texto_atualizado

            quantidade += quantidade_local

        # -----------------------------------------------------
        # TABELAS
        # -----------------------------------------------------

        for tabela in documento.tables:
            for linha in tabela.rows:
                for celula in linha.cells:
                    for paragrafo in celula.paragraphs:
                        texto_original = paragrafo.text

                        if not texto_original.strip():
                            continue

                        texto_atualizado, quantidade_local = (
                            atualizar_texto(texto_original)
                        )

                        if texto_atualizado != texto_original:
                            paragrafo.text = texto_atualizado

                        quantidade += quantidade_local

        self.logger.info(
            "Atualização automática concluída. "
            "%d substituição(ões) realizada(s).",
            quantidade,
        )

        return quantidade