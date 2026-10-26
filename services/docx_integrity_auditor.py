"""
Agenda Universal PRO
Sprint 7.1 - Auditoria de integridade de pacotes DOCX.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from zipfile import BadZipFile, ZipFile


@dataclass(frozen=True)
class RelatorioIntegridadeDOCX:
    """Resultado da verificacao de um pacote DOCX."""

    arquivo: str
    zip_valido: bool
    componentes: tuple[str, ...]
    total_componentes: int
    componentes_xml: int
    componentes_midia: int
    arquivos_corrompidos: tuple[str, ...]


class DocxIntegrityAuditor:
    """Inspeciona pacotes DOCX sem alterar os arquivos."""

    @staticmethod
    def auditar(
        caminho: str | Path,
    ) -> RelatorioIntegridadeDOCX:
        """Verifica a integridade ZIP e lista os componentes."""

        arquivo = Path(caminho)

        if not arquivo.is_file():
            raise FileNotFoundError(
                f"Documento nao encontrado: {arquivo}"
            )

        componentes: tuple[str, ...] = ()
        corrompidos: tuple[str, ...] = ()
        zip_valido = False

        try:
            with ZipFile(arquivo, "r") as pacote:
                nomes = tuple(
                    sorted(
                        nome
                        for nome in pacote.namelist()
                        if not nome.endswith("/")
                    )
                )

                componentes = nomes

                arquivo_corrompido = pacote.testzip()

                if arquivo_corrompido is None:
                    zip_valido = True
                else:
                    corrompidos = (arquivo_corrompido,)

        except BadZipFile:
            zip_valido = False

        componentes_xml = sum(
            nome.lower().endswith((".xml", ".rels"))
            for nome in componentes
        )

        componentes_midia = sum(
            nome.startswith("word/media/")
            for nome in componentes
        )

        return RelatorioIntegridadeDOCX(
            arquivo=str(arquivo),
            zip_valido=zip_valido,
            componentes=componentes,
            total_componentes=len(componentes),
            componentes_xml=componentes_xml,
            componentes_midia=componentes_midia,
            arquivos_corrompidos=corrompidos,
        )