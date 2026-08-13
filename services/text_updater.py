"""
Agenda Universal PRO
Arquivo: services/text_updater.py

Serviço responsável por localizar e atualizar datas
nos parágrafos de um documento Word.
"""

from __future__ import annotations

from logging import Logger

from docx.document import Document as DocxDocument

from core.date_parser import DateParser
from services.logger_service import LoggerService


class TextUpdater:
    """Localiza e atualiza datas existentes nos parágrafos do documento."""

    def __init__(self) -> None:
        self.logger: Logger = LoggerService.get_logger()

    def localizar_datas(
        self, documento: DocxDocument
    ) -> list[tuple[int, str, list[str]]]:
        """
        Percorre todos os parágrafos procurando datas.

        Args:
            documento: Documento Word aberto.

        Returns:
            Lista contendo:
                (índice do parágrafo, texto, datas encontradas)
        """

        ocorrencias: list[tuple[int, str, list[str]]] = []

        self.logger.info("Iniciando leitura dos parágrafos.")

        for indice, paragrafo in enumerate(documento.paragraphs):
            texto = paragrafo.text.strip()

            if not texto:
                continue

            datas = DateParser.encontrar_datas(texto)

            if datas:
                ocorrencias.append((indice, texto, datas))

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

    def atualizar_datas(
        self,
        documento: DocxDocument,
        substituicoes: dict[str, str],
    ) -> int:
        """
        Substitui datas nos parágrafos do documento.

        Args:
            documento: Documento Word aberto.
            substituicoes: Dicionário no formato:
                {"data_antiga": "data_nova"}

        Returns:
            Quantidade de substituições realizadas.
        """

        quantidade = 0

        self.logger.info("Iniciando atualização das datas.")

        for paragrafo in documento.paragraphs:
            texto_original = paragrafo.text

            if not texto_original.strip():
                continue

            texto_atualizado = texto_original

            for data_antiga, data_nova in substituicoes.items():
                ocorrencias = texto_atualizado.count(data_antiga)

                if ocorrencias:
                    texto_atualizado = texto_atualizado.replace(
                        data_antiga,
                        data_nova,
                    )
                    quantidade += ocorrencias

            if texto_atualizado != texto_original:
                paragrafo.text = texto_atualizado

        self.logger.info(
            "Atualização concluída. %d substituição(ões) realizada(s).",
            quantidade,
        )

        return quantidade