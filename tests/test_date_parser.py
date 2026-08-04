from core.date_parser import DateParser


def test_encontrar_datas():
    texto = "Reunião em 05/01/2027 e audiência em 10/02/2027"

    resultado = DateParser.encontrar_datas(texto)

    assert resultado == [
        "05/01/2027",
        "10/02/2027",
    ]


def test_validar_data_valida():
    assert DateParser.validar_data("28/02/2027")


def test_validar_data_invalida():
    assert not DateParser.validar_data("29/02/2027")