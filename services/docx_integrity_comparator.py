"""
Agenda Universal PRO
Sprint 7.1 - Comparacao estrutural de pacotes DOCX.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from services.docx_integrity_auditor import DocxIntegrityAuditor


@dataclass(frozen=True)
class RelatorioComparacaoDOCX:
    """Resultado da comparacao de componentes DOCX."""

    original_valido: bool
    atualizado_valido: bool
    componentes_preservados: tuple[str, ...]
    componentes_removidos: tuple[str, ...]
    componentes_adicionados: tuple[str, ...]
    estrutura_componentes_igual: bool


class DocxIntegrityComparator:
    """Compara inventarios DOCX sem modificar os arquivos."""

    @staticmethod
    def comparar(
        original: str | Path,
        atualizado: str | Path,
    ) -> RelatorioComparacaoDOCX:
        """Compara os componentes internos de dois pacotes DOCX."""

        auditor = DocxIntegrityAuditor()

        relatorio_original = auditor.auditar(original)
        relatorio_atualizado = auditor.auditar(atualizado)

        componentes_original = set(relatorio_original.componentes)
        componentes_atualizado = set(relatorio_atualizado.componentes)

        preservados = tuple(
            sorted(componentes_original & componentes_atualizado)
        )

        removidos = tuple(
            sorted(componentes_original - componentes_atualizado)
        )

        adicionados = tuple(
            sorted(componentes_atualizado - componentes_original)
        )

        estrutura_igual = (
            relatorio_original.zip_valido
            and relatorio_atualizado.zip_valido
            and not removidos
            and not adicionados
        )

        return RelatorioComparacaoDOCX(
            original_valido=relatorio_original.zip_valido,
            atualizado_valido=relatorio_atualizado.zip_valido,
            componentes_preservados=preservados,
            componentes_removidos=removidos,
            componentes_adicionados=adicionados,
            estrutura_componentes_igual=estrutura_igual,
        )