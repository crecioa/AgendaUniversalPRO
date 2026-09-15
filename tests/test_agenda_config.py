"""
Agenda Universal PRO
Arquivo: tests/test_agenda_config.py

Testes da configuração de execução da agenda.

Sprint 4.18:
- Fortalece os testes da AgendaConfig.
- Valida normalização dos caminhos.
- Valida propriedades dos nomes dos arquivos.
- Valida a imutabilidade da configuração.
"""

from pathlib import Path

import pytest

from config.agenda_config import AgendaConfig


def test_cria_configuracao_com_paths() -> None:
    """Valida criação da configuração utilizando objetos Path."""

    origem = Path("modelos") / "agenda_2026.docx"
    destino = Path("output") / "agenda_2027.docx"

    configuracao = AgendaConfig(
        arquivo_origem=origem,
        arquivo_destino=destino,
        ano_origem=2026,
        ano_destino=2027,
    )

    assert configuracao.arquivo_origem == origem
    assert configuracao.arquivo_destino == destino
    assert configuracao.ano_origem == 2026
    assert configuracao.ano_destino == 2027


def test_normaliza_caminhos() -> None:
    """Valida a normalização dos caminhos no pós-inicializador."""

    origem = Path("modelos") / "agenda_2026.docx"
    destino = Path("output") / "agenda_2027.docx"

    configuracao = AgendaConfig(
        arquivo_origem=origem,
        arquivo_destino=destino,
        ano_origem=2026,
        ano_destino=2027,
    )

    assert isinstance(
        configuracao.arquivo_origem,
        Path,
    )

    assert isinstance(
        configuracao.arquivo_destino,
        Path,
    )

    assert configuracao.arquivo_origem == origem
    assert configuracao.arquivo_destino == destino


def test_retorna_nome_do_arquivo_de_origem() -> None:
    """Valida a propriedade nome_arquivo_origem."""

    configuracao = AgendaConfig(
        arquivo_origem=Path(
            "modelos",
            "agenda_2026.docx",
        ),
        arquivo_destino=Path(
            "output",
            "agenda_2027.docx",
        ),
        ano_origem=2026,
        ano_destino=2027,
    )

    assert (
        configuracao.nome_arquivo_origem
        == "agenda_2026.docx"
    )


def test_retorna_nome_do_arquivo_de_destino() -> None:
    """Valida a propriedade nome_arquivo_destino."""

    configuracao = AgendaConfig(
        arquivo_origem=Path(
            "modelos",
            "agenda_2026.docx",
        ),
        arquivo_destino=Path(
            "output",
            "agenda_2027.docx",
        ),
        ano_origem=2026,
        ano_destino=2027,
    )

    assert (
        configuracao.nome_arquivo_destino
        == "agenda_2027.docx"
    )


def test_configuracao_permanece_imutavel() -> None:
    """Valida que AgendaConfig permanece imutável."""

    configuracao = AgendaConfig(
        arquivo_origem=Path("agenda_2026.docx"),
        arquivo_destino=Path("agenda_2027.docx"),
        ano_origem=2026,
        ano_destino=2027,
    )

    with pytest.raises(AttributeError):
        configuracao.ano_destino = 2028  # type: ignore[misc]


def test_preserva_anos_informados() -> None:
    """Valida os anos de origem e destino."""

    configuracao = AgendaConfig(
        arquivo_origem=Path("agenda_2025.docx"),
        arquivo_destino=Path("agenda_2026.docx"),
        ano_origem=2025,
        ano_destino=2026,
    )

    assert configuracao.ano_origem == 2025
    assert configuracao.ano_destino == 2026