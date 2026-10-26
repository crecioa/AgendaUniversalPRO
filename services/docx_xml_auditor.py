"""
Agenda Universal PRO
Sprint 7.2 - Auditoria de componentes XML DOCX.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile


@dataclass(frozen=True)
class RelatorioXMLDOCX:
    """Resultado da verificacao dos componentes XML."""

    arquivo: str
    componentes_xml: int
    componentes_validos: int
    componentes_invalidos: tuple[str, ...]
    xml_valido: bool


class DocxXMLAuditor:
    """Verifica a sintaxe XML dos componentes de um DOCX."""

    @staticmethod
    def auditar(caminho: str | Path) -> RelatorioXMLDOCX:
        """Analisa componentes XML sem modificar o arquivo."""

        arquivo = Path(caminho)

        if not arquivo.is_file():
            raise FileNotFoundError(
                f"Documento nao encontrado: {arquivo}"
            )

        validos = 0
        invalidos: list[str] = []

        with ZipFile(arquivo, "r") as pacote:
            componentes = sorted(
                nome
                for nome in pacote.namelist()
                if nome.lower().endswith((".xml", ".rels"))
            )

            for componente in componentes:
                try:
                    ElementTree.fromstring(
                        pacote.read(componente)
                    )
                    validos += 1

                except ElementTree.ParseError as erro:
                    invalidos.append(
                        f"{componente}: {erro}"
                    )

        return RelatorioXMLDOCX(
            arquivo=str(arquivo),
            componentes_xml=len(componentes),
            componentes_validos=validos,
            componentes_invalidos=tuple(invalidos),
            xml_valido=not invalidos,
        )