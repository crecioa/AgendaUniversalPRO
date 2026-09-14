"""
Agenda Universal PRO
Arquivo: tests/test_holiday_service.py

Testes do serviço responsável pela consulta de feriados nacionais.

Sprint 4.13:
- Testa identificação dos feriados nacionais fixos.
- Testa obtenção do nome dos feriados.
- Testa datas que não são feriados.
- Testa diferentes feriados ao longo do ano.
"""

from datetime import date

from core.holiday_service import HolidayService


def test_eh_feriado_confraternizacao_universal() -> None:
    """Testa o feriado de 1º de janeiro."""

    resultado = HolidayService.eh_feriado(
        date(2027, 1, 1),
    )

    assert resultado is True


def test_eh_feriado_tiradentes() -> None:
    """Testa o feriado de Tiradentes."""

    resultado = HolidayService.eh_feriado(
        date(2027, 4, 21),
    )

    assert resultado is True


def test_eh_feriado_dia_do_trabalhador() -> None:
    """Testa o feriado do Dia do Trabalhador."""

    resultado = HolidayService.eh_feriado(
        date(2027, 5, 1),
    )

    assert resultado is True


def test_eh_feriado_independencia() -> None:
    """Testa o feriado da Independência do Brasil."""

    resultado = HolidayService.eh_feriado(
        date(2027, 9, 7),
    )

    assert resultado is True


def test_eh_feriado_nossa_senhora_aparecida() -> None:
    """Testa o feriado de Nossa Senhora Aparecida."""

    resultado = HolidayService.eh_feriado(
        date(2027, 10, 12),
    )

    assert resultado is True


def test_eh_feriado_finados() -> None:
    """Testa o feriado de Finados."""

    resultado = HolidayService.eh_feriado(
        date(2027, 11, 2),
    )

    assert resultado is True


def test_eh_feriado_proclamacao_da_republica() -> None:
    """Testa o feriado da Proclamação da República."""

    resultado = HolidayService.eh_feriado(
        date(2027, 11, 15),
    )

    assert resultado is True


def test_eh_feriado_natal() -> None:
    """Testa o feriado de Natal."""

    resultado = HolidayService.eh_feriado(
        date(2027, 12, 25),
    )

    assert resultado is True


def test_nao_eh_feriado() -> None:
    """Testa uma data comum que não é feriado."""

    resultado = HolidayService.eh_feriado(
        date(2027, 1, 4),
    )

    assert resultado is False


def test_nome_feriado_confraternizacao_universal() -> None:
    """Testa o nome do feriado de 1º de janeiro."""

    resultado = HolidayService.nome_feriado(
        date(2027, 1, 1),
    )

    assert resultado == "Confraternização Universal"


def test_nome_feriado_tiradentes() -> None:
    """Testa o nome do feriado de Tiradentes."""

    resultado = HolidayService.nome_feriado(
        date(2027, 4, 21),
    )

    assert resultado == "Tiradentes"


def test_nome_feriado_dia_do_trabalhador() -> None:
    """Testa o nome do feriado do Dia do Trabalhador."""

    resultado = HolidayService.nome_feriado(
        date(2027, 5, 1),
    )

    assert resultado == "Dia do Trabalhador"


def test_nome_feriado_independencia() -> None:
    """Testa o nome do feriado da Independência do Brasil."""

    resultado = HolidayService.nome_feriado(
        date(2027, 9, 7),
    )

    assert resultado == "Independência do Brasil"


def test_nome_feriado_nossa_senhora_aparecida() -> None:
    """Testa o nome do feriado de Nossa Senhora Aparecida."""

    resultado = HolidayService.nome_feriado(
        date(2027, 10, 12),
    )

    assert resultado == "Nossa Senhora Aparecida"


def test_nome_feriado_finados() -> None:
    """Testa o nome do feriado de Finados."""

    resultado = HolidayService.nome_feriado(
        date(2027, 11, 2),
    )

    assert resultado == "Finados"


def test_nome_feriado_proclamacao_da_republica() -> None:
    """Testa o nome do feriado da Proclamação da República."""

    resultado = HolidayService.nome_feriado(
        date(2027, 11, 15),
    )

    assert resultado == "Proclamação da República"


def test_nome_feriado_natal() -> None:
    """Testa o nome do feriado de Natal."""

    resultado = HolidayService.nome_feriado(
        date(2027, 12, 25),
    )

    assert resultado == "Natal"


def test_nome_feriado_data_normal() -> None:
    """Testa retorno nulo para uma data sem feriado."""

    resultado = HolidayService.nome_feriado(
        date(2027, 1, 4),
    )

    assert resultado is None


def test_eh_feriado_mesmo_dia_em_outro_ano() -> None:
    """Testa que o feriado fixo é reconhecido em outro ano."""

    resultado = HolidayService.eh_feriado(
        date(2030, 12, 25),
    )

    assert resultado is True


def test_nome_feriado_mesmo_dia_em_outro_ano() -> None:
    """Testa o nome de um feriado fixo em outro ano."""

    resultado = HolidayService.nome_feriado(
        date(2030, 12, 25),
    )

    assert resultado == "Natal"

