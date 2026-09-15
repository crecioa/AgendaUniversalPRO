from datetime import datetime

from core.date_parser import DateParser


def test_encontrar_datas():
    texto = (
        "Reunião em 05/01/2027 e audiência em 10/02/2027."
    )

    resultado = DateParser.encontrar_datas(texto)

    assert resultado == ["05/01/2027", "10/02/2027"]


def test_encontrar_datas_sem_datas():
    texto = "Nenhuma data foi informada neste texto."

    resultado = DateParser.encontrar_datas(texto)

    assert resultado == []


def test_encontrar_varias_datas():
    texto = (
        "05/01/2027, 10/02/2027 e 25/12/2027 "
        "são datas importantes."
    )

    resultado = DateParser.encontrar_datas(texto)

    assert resultado == [
        "05/01/2027",
        "10/02/2027",
        "25/12/2027",
    ]


def test_validar_data_valida():
    assert DateParser.validar_data("05/01/2027") is True


def test_validar_data_invalida():
    assert DateParser.validar_data("31/02/2027") is False


def test_validar_data_com_dia_e_mes_sem_zero():
    assert DateParser.validar_data("5/1/2027") is True


def test_converter_data_valida():
    resultado = DateParser.converter_data("05/01/2027")

    assert resultado == datetime(2027, 1, 5)


def test_converter_data_invalida():
    resultado = DateParser.converter_data("31/02/2027")

    assert resultado is None


def test_atualizar_ano_data_valida():
    resultado = DateParser.atualizar_ano(
        "05/01/2026",
        2027,
    )

    assert resultado == "05/01/2027"


def test_atualizar_ano_data_invalida():
    resultado = DateParser.atualizar_ano(
        "31/02/2026",
        2027,
    )

    assert resultado is None


def test_atualizar_ano_29_fevereiro_para_ano_nao_bissexto():
    resultado = DateParser.atualizar_ano(
        "29/02/2024",
        2025,
    )

    assert resultado is None


def test_atualizar_ano_29_fevereiro_para_ano_bissexto():
    resultado = DateParser.atualizar_ano(
        "29/02/2024",
        2028,
    )

    assert resultado == "29/02/2028"