"""
Agenda Universal PRO
Sprint 7.1 - Auditoria de formatacao de documentos Word.
"""

from __future__ import annotations

from dataclasses import dataclass

from collections.abc import Iterator

from docx.document import Document as DocxDocument
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph


@dataclass(frozen=True)
class RelatorioFormatacao:
    """Resumo de formatacao explicita dos runs."""

    paragrafos_analisados: int
    runs_analisados: int
    runs_negrito: int
    runs_italico: int
    runs_sublinhado: int
    estilos_paragrafo: tuple[str, ...]


class FormattingAuditor:
    """Audita formatacao sem modificar o documento."""

    @classmethod
    def _iterar_tabela(
        cls,
        tabela: Table,
        celulas_visitadas: set[int],
    ) -> Iterator[Paragraph]:
        """Percorre tabelas, inclusive aninhadas, sem repetir celulas."""

        for linha in tabela.rows:
            for celula in linha.cells:
                identificador = id(celula._tc)

                if identificador in celulas_visitadas:
                    continue

                celulas_visitadas.add(identificador)

                for bloco in celula.iter_inner_content():
                    if isinstance(bloco, Paragraph):
                        yield bloco

                    elif isinstance(bloco, Table):
                        yield from cls._iterar_tabela(
                            bloco,
                            celulas_visitadas,
                        )

    @classmethod
    def _iterar_paragrafos(
        cls,
        documento: DocxDocument,
    ) -> Iterator[Paragraph]:
        """Percorre paragrafos principais e tabelas complexas."""

        celulas_visitadas: set[int] = set()

        for bloco in documento.iter_inner_content():
            if isinstance(bloco, Paragraph):
                yield bloco

            elif isinstance(bloco, Table):
                yield from cls._iterar_tabela(
                    bloco,
                    celulas_visitadas,
                )

    def auditar(self, documento: DocxDocument) -> RelatorioFormatacao:
        """Produz um resumo da formatacao explicita."""

        paragrafos: list[Paragraph] = list(
            self._iterar_paragrafos(documento)
        )

        runs = [
            run
            for paragrafo in paragrafos
            for run in paragrafo.runs
        ]

        estilos = tuple(
            sorted({
                estilo.name
                for paragrafo in paragrafos
                if (estilo := paragrafo.style) is not None
            })
        )

        return RelatorioFormatacao(
            paragrafos_analisados=len(paragrafos),
            runs_analisados=len(runs),
            runs_negrito=sum(
                run.bold is True
                for run in runs
            ),
            runs_italico=sum(
                run.italic is True
                for run in runs
            ),
            runs_sublinhado=sum(
                run.underline is True
                for run in runs
            ),
            estilos_paragrafo=estilos,
        )