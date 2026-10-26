"""
Agenda Universal PRO
Sprint 7.2 - Auditoria de relacionamentos DOCX.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from posixpath import dirname, join, normpath
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree
from zipfile import ZipFile


NAMESPACE_RELACIONAMENTOS = (
    "http://schemas.openxmlformats.org/package/2006/relationships"
)


@dataclass(frozen=True)
class RelatorioRelacionamentosDOCX:
    """Resultado da auditoria de relacionamentos DOCX."""

    arquivo: str
    arquivos_relacionamentos: int
    relacionamentos_internos: int
    relacionamentos_externos: int
    relacionamentos_invalidos: tuple[str, ...]
    xml_invalidos: tuple[str, ...]
    relacionamentos_validos: bool


class DocxRelationshipAuditor:
    """Audita relacionamentos internos de pacotes DOCX."""

    @staticmethod
    def _origem_relacionamento(caminho_rels: str) -> str:
        """Identifica o componente de origem de um arquivo .rels."""

        if caminho_rels == "_rels/.rels":
            return ""

        pasta = dirname(caminho_rels)

        if not pasta.endswith("/_rels"):
            raise ValueError(
                f"Caminho de relacionamentos invalido: {caminho_rels}"
            )

        pasta_origem = dirname(pasta)
        nome = caminho_rels.rsplit("/", 1)[-1]

        if not nome.endswith(".rels"):
            raise ValueError(
                f"Arquivo de relacionamentos invalido: {caminho_rels}"
            )

        componente = nome[:-5]

        return (
            join(pasta_origem, componente)
            if pasta_origem
            else componente
        )

    @staticmethod
    def _resolver_destino(
        origem: str,
        destino: str,
    ) -> str:
        """Resolve o destino interno de um relacionamento."""

        caminho = unquote(urlsplit(destino).path)

        if caminho.startswith("/"):
            return normpath(caminho.lstrip("/"))

        return normpath(join(dirname(origem), caminho))

    @staticmethod
    def auditar(
        caminho: str | Path,
    ) -> RelatorioRelacionamentosDOCX:
        """Inspeciona relacionamentos sem alterar o DOCX."""

        arquivo = Path(caminho)

        if not arquivo.is_file():
            raise FileNotFoundError(
                f"Documento nao encontrado: {arquivo}"
            )

        internos = 0
        externos = 0
        invalidos: list[str] = []
        xml_invalidos: list[str] = []

        with ZipFile(arquivo, "r") as pacote:
            componentes = {
                nome
                for nome in pacote.namelist()
                if not nome.endswith("/")
            }

            arquivos_rels = sorted(
                nome
                for nome in componentes
                if nome.endswith(".rels")
                and (
                    nome == "_rels/.rels"
                    or "/_rels/" in nome
                )
            )

            for caminho_rels in arquivos_rels:
                try:
                    origem = (
                        DocxRelationshipAuditor
                        ._origem_relacionamento(caminho_rels)
                    )

                    raiz = ElementTree.fromstring(
                        pacote.read(caminho_rels)
                    )

                    if raiz.tag != (
                        f"{{{NAMESPACE_RELACIONAMENTOS}}}Relationships"
                    ):
                        raise ValueError(
                            "Elemento raiz de relacionamentos invalido"
                        )

                except (ElementTree.ParseError, ValueError) as erro:
                    xml_invalidos.append(
                        f"{caminho_rels}: {erro}"
                    )
                    continue

                for relacionamento in raiz:
                    if relacionamento.tag != (
                        f"{{{NAMESPACE_RELACIONAMENTOS}}}Relationship"
                    ):
                        invalidos.append(
                            f"{caminho_rels}: elemento inesperado"
                        )
                        continue

                    identificador = relacionamento.get("Id", "")
                    destino = relacionamento.get("Target", "")
                    tipo = relacionamento.get("Type", "")
                    modo = relacionamento.get("TargetMode", "Internal")

                    if not identificador or not destino or not tipo:
                        invalidos.append(
                            f"{caminho_rels}: relacionamento incompleto"
                        )
                        continue

                    if modo == "External":
                        externos += 1
                        continue

                    if modo != "Internal":
                        invalidos.append(
                            f"{caminho_rels}: TargetMode invalido"
                        )
                        continue

                    internos += 1

                    destino_resolvido = (
                        DocxRelationshipAuditor._resolver_destino(
                            origem,
                            destino,
                        )
                    )

                    if (
                        destino_resolvido == ".."
                        or destino_resolvido.startswith("../")
                        or destino_resolvido not in componentes
                    ):
                        invalidos.append(
                            f"{caminho_rels} [{identificador}] "
                            f"-> {destino_resolvido}"
                        )

        return RelatorioRelacionamentosDOCX(
            arquivo=str(arquivo),
            arquivos_relacionamentos=len(arquivos_rels),
            relacionamentos_internos=internos,
            relacionamentos_externos=externos,
            relacionamentos_invalidos=tuple(invalidos),
            xml_invalidos=tuple(xml_invalidos),
            relacionamentos_validos=(
                not invalidos and not xml_invalidos
            ),
        )