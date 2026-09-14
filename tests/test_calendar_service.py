"""
Agenda Universal PRO
Arquivo: tests/test_calendar_service.py

Testes do serviço responsável pelas operações de calendário.

Sprint 4.12:
- Testa identificação do dia da semana.
- Testa identificação de fim de semana.
- Testa identificação de feriados.
- Testa obtenção do nome do feriado.
- Testa resumo completo de uma data.
"""

from datetime import date

from core.calendar_service import CalendarService


def test_dia_semana_segunda_feira() -> None:
    """Testa identificação de segunda-feira."""

    resultado = CalendarService.dia_semana(
        date(2027, 1, 4),
    )

    assert resultado == "Segunda-feira"


def test_dia_semana_sabado() -> None:
    """Testa identificação de sábado."""

    resultado = CalendarService.dia_semana(
        date(2027, 1, 9),
    )

    assert resultado == "Sábado"


def test_dia_semana_domingo() -> None:
    """Testa identificação de domingo."""

    resultado = CalendarService.dia_semana(
        date(2027, 1, 10),
    )

    assert resultado == "Domingo"


def test_fim_de_semana_sabado() -> None:
    """Testa que sábado é considerado fim de semana."""

    resultado = CalendarService.fim_de_semana(
        date(2027, 1, 9),
    )

    assert resultado is True


def test_fim_de_semana_domingo() -> None:
    """Testa que domingo é considerado fim de semana."""

    resultado = CalendarService.fim_de_semana(
        date(2027, 1, 10),
    )

    assert resultado is True


def test_fim_de_semana_dia_util() -> None:
    """Testa que dia útil não é fim de semana."""

    resultado = CalendarService.fim_de_semana(
        date(2027, 1, 8),
    )

    assert resultado is False


def test_eh_feriado() -> None:
    """Testa identificação de um feriado nacional."""

    resultado = CalendarService.eh_feriado(
        date(2027, 1, 1),
    )

    assert resultado is True


def test_nao_eh_feriado() -> None:
    """Testa uma data que não é feriado."""

    resultado = CalendarService.eh_feriado(
        date(2027, 1, 4),
    )

    assert resultado is False


def test_nome_feriado() -> None:
    """Testa obtenção do nome de um feriado."""

    resultado = CalendarService.nome_feriado(
        date(2027, 1, 1),
    )

    assert resultado == "Confraternização Universal"


def test_nome_feriado_data_normal() -> None:
    """Testa retorno nulo para uma data sem feriado."""

    resultado = CalendarService.nome_feriado(
        date(2027, 1, 4),
    )

    assert resultado is None


def test_resumo_data_util() -> None:
    """Testa resumo completo de uma data comum."""

    resultado = CalendarService.resumo_data(
        date(2027, 1, 4),
    )

    assert resultado == {
        "data": "04/01/2027",
        "dia_semana": "Segunda-feira",
        "fim_de_semana": False,
        "feriado": False,
        "nome_feriado": None,
    }


def test_resumo_data_feriado() -> None:
    """Testa resumo completo de um feriado."""

    resultado = CalendarService.resumo_data(
        date(2027, 1, 1),
    )

    assert resultado == {
        "data": "01/01/2027",
        "dia_semana": "Sexta-feira",
        "fim_de_semana": False,
        "feriado": True,
        "nome_feriado": "Confraternização Universal",
    }


def test_resumo_data_fim_de_semana() -> None:
    """Testa resumo completo de um domingo."""

    resultado = CalendarService.resumo_data(
        date(2027, 1, 10),
    )

    assert resultado == {
        "data": "10/01/2027",
        "dia_semana": "Domingo",
        "fim_de_semana": True,
        "feriado": False,
        "nome_feriado": None,
    }