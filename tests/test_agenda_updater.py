"""
Agenda Universal PRO

Arquivo: tests/test_agenda_updater.py

Testes do serviço AgendaUpdater.

Sprint 4.15:

* Testa abertura da agenda.
* Testa atualização de datas.
* Testa atualização automática de ano.
* Testa validações de origem.
* Testa validações de destino.
* Testa validações de ano.
* Testa propagação de exceções.
"""

from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest

from core.agenda_updater import AgendaUpdater


def criar_updater_mockado() -> Any:
    """Cria um AgendaUpdater com dependências simuladas."""
    updater = AgendaUpdater()

    updater.backup_service = Mock()
    updater.word_service = Mock()
    updater.text_updater = Mock()

    return updater


def test_abrir_agenda_com_sucesso(tmp_path: Path) -> None:
    """Testa abertura de uma agenda com sucesso."""
    arquivo = tmp_path / "agenda.docx"
    arquivo.write_text("arquivo de teste")

    documento = Mock()

    updater = criar_updater_mockado()

    abrir_documento = Mock(return_value=documento)
    localizar_datas = Mock(
        return_value=[
            (
                0,
                "Audiência em 05/01/2027.",
                ["05/01/2027"],
            )
        ]
    )

    updater.word_service.abrir_documento = abrir_documento
    updater.text_updater.localizar_datas = localizar_datas

    resultado = updater.abrir_agenda(arquivo)

    assert resultado is documento

    updater.backup_service.criar_backup.assert_called_once_with(
        arquivo
    )

    abrir_documento.assert_called_once_with(arquivo)

    localizar_datas.assert_called_once_with(documento)


def test_abrir_agenda_propaga_erro_do_backup(
    tmp_path: Path,
) -> None:
    """Testa propagação de erro durante a criação do backup."""
    arquivo = tmp_path / "agenda.docx"
    arquivo.write_text("arquivo de teste")

    updater = criar_updater_mockado()

    criar_backup = Mock(
        side_effect=RuntimeError("erro no backup")
    )
    abrir_documento = Mock()

    updater.backup_service.criar_backup = criar_backup
    updater.word_service.abrir_documento = abrir_documento

    with pytest.raises(RuntimeError, match="erro no backup"):
        updater.abrir_agenda(arquivo)

    abrir_documento.assert_not_called()


def test_abrir_agenda_propaga_erro_ao_abrir_documento(
    tmp_path: Path,
) -> None:
    """Testa propagação de erro ao abrir o documento."""
    arquivo = tmp_path / "agenda.docx"
    arquivo.write_text("arquivo de teste")

    updater = criar_updater_mockado()

    abrir_documento = Mock(
        side_effect=RuntimeError("erro ao abrir")
    )
    updater.word_service.abrir_documento = abrir_documento

    with pytest.raises(RuntimeError, match="erro ao abrir"):
        updater.abrir_agenda(arquivo)


def test_atualizar_agenda_com_sucesso(
    tmp_path: Path,
) -> None:
    """Testa atualização completa da agenda."""
    arquivo = tmp_path / "agenda.docx"
    destino = tmp_path / "agenda_atualizada.docx"

    arquivo.write_text("arquivo de teste")

    documento = Mock()

    updater = criar_updater_mockado()

    abrir_documento = Mock(return_value=documento)
    atualizar_datas = Mock(return_value=3)
    salvar_documento = Mock()

    updater.word_service.abrir_documento = abrir_documento
    updater.text_updater.atualizar_datas = atualizar_datas
    updater.word_service.salvar_documento = salvar_documento

    substituicoes = {
        "05/01/2027": "05/01/2028",
        "10/02/2027": "10/02/2028",
        "15/03/2027": "15/03/2028",
    }

    quantidade = updater.atualizar_agenda(
        arquivo,
        substituicoes,
        destino,
    )

    assert quantidade == 3

    updater.backup_service.criar_backup.assert_called_once_with(
        arquivo
    )

    abrir_documento.assert_called_once_with(arquivo)

    atualizar_datas.assert_called_once_with(
        documento,
        substituicoes,
    )

    salvar_documento.assert_called_once_with(
        documento,
        destino,
    )


def test_atualizar_agenda_propaga_erro_na_atualizacao(
    tmp_path: Path,
) -> None:
    """Testa propagação de erro durante a atualização."""
    arquivo = tmp_path / "agenda.docx"
    destino = tmp_path / "agenda_atualizada.docx"

    arquivo.write_text("arquivo de teste")

    updater = criar_updater_mockado()

    documento = Mock()

    abrir_documento = Mock(return_value=documento)
    atualizar_datas = Mock(
        side_effect=RuntimeError("erro na atualização")
    )
    salvar_documento = Mock()

    updater.word_service.abrir_documento = abrir_documento
    updater.text_updater.atualizar_datas = atualizar_datas
    updater.word_service.salvar_documento = salvar_documento

    with pytest.raises(
        RuntimeError,
        match="erro na atualização",
    ):
        updater.atualizar_agenda(
            arquivo,
            {"05/01/2027": "05/01/2028"},
            destino,
        )

    salvar_documento.assert_not_called()


def test_atualizar_ano_com_sucesso(
    tmp_path: Path,
) -> None:
    """Testa atualização automática de ano."""
    arquivo = tmp_path / "agenda.docx"
    destino = tmp_path / "agenda_2027.docx"

    arquivo.write_text("arquivo de teste")

    documento = Mock()

    updater = criar_updater_mockado()

    abrir_documento = Mock(return_value=documento)
    atualizar_ano = Mock(return_value=2)
    salvar_documento = Mock()

    updater.word_service.abrir_documento = abrir_documento
    updater.text_updater.atualizar_ano = atualizar_ano
    updater.word_service.salvar_documento = salvar_documento

    quantidade = updater.atualizar_ano(
        arquivo,
        2026,
        2027,
        destino,
    )

    assert quantidade == 2

    updater.backup_service.criar_backup.assert_called_once_with(
        arquivo
    )

    abrir_documento.assert_called_once_with(arquivo)

    atualizar_ano.assert_called_once_with(
        documento,
        2026,
        2027,
    )

    salvar_documento.assert_called_once_with(
        documento,
        destino,
    )


def test_atualizar_ano_propaga_erro_na_atualizacao(
    tmp_path: Path,
) -> None:
    """Testa propagação de erro durante atualização de ano."""
    arquivo = tmp_path / "agenda.docx"
    destino = tmp_path / "agenda_2027.docx"

    arquivo.write_text("arquivo de teste")

    updater = criar_updater_mockado()

    documento = Mock()

    abrir_documento = Mock(return_value=documento)
    atualizar_ano = Mock(
        side_effect=RuntimeError("erro na atualização do ano")
    )
    salvar_documento = Mock()

    updater.word_service.abrir_documento = abrir_documento
    updater.text_updater.atualizar_ano = atualizar_ano
    updater.word_service.salvar_documento = salvar_documento

    with pytest.raises(
        RuntimeError,
        match="erro na atualização do ano",
    ):
        updater.atualizar_ano(
            arquivo,
            2026,
            2027,
            destino,
        )

    salvar_documento.assert_not_called()


def test_validar_arquivo_origem_inexistente(
    tmp_path: Path,
) -> None:
    """Testa arquivo de origem inexistente."""
    arquivo = tmp_path / "nao_existe.docx"

    with pytest.raises(
        FileNotFoundError,
        match="Arquivo de origem não encontrado",
    ):
        AgendaUpdater._validar_arquivo_origem(arquivo)


def test_validar_arquivo_origem_diretorio(
    tmp_path: Path,
) -> None:
    """Testa quando a origem é um diretório."""
    diretorio = tmp_path / "agenda.docx"
    diretorio.mkdir()

    with pytest.raises(
        ValueError,
        match="não é um arquivo",
    ):
        AgendaUpdater._validar_arquivo_origem(diretorio)


def test_validar_arquivo_origem_extensao_invalida(
    tmp_path: Path,
) -> None:
    """Testa extensão inválida do arquivo de origem."""
    arquivo = tmp_path / "agenda.pdf"
    arquivo.write_text("arquivo de teste")

    with pytest.raises(
        ValueError,
        match="extensão .docx",
    ):
        AgendaUpdater._validar_arquivo_origem(arquivo)


def test_validar_destino_igual_origem(
    tmp_path: Path,
) -> None:
    """Testa bloqueio de sobrescrita do arquivo original."""
    origem = tmp_path / "agenda.docx"

    with pytest.raises(
        ValueError,
        match="não pode ser igual ao arquivo original",
    ):
        AgendaUpdater._validar_destino(
            origem,
            origem,
        )


def test_validar_destino_extensao_invalida(
    tmp_path: Path,
) -> None:
    """Testa extensão inválida do destino."""
    origem = tmp_path / "agenda.docx"
    destino = tmp_path / "agenda.pdf"

    with pytest.raises(
        ValueError,
        match="extensão .docx",
    ):
        AgendaUpdater._validar_destino(
            origem,
            destino,
        )


def test_validar_anos_validos() -> None:
    """Testa anos válidos."""
    AgendaUpdater._validar_anos(
        2026,
        2027,
    )


def test_validar_ano_origem_nao_inteiro() -> None:
    """Testa ano de origem com tipo inválido."""
    with pytest.raises(
        ValueError,
        match="ano de origem deve ser um número inteiro",
    ):
        AgendaUpdater._validar_anos(
            "2026",  # type: ignore[arg-type]
            2027,
        )


def test_validar_ano_destino_nao_inteiro() -> None:
    """Testa ano de destino com tipo inválido."""
    with pytest.raises(
        ValueError,
        match="ano de destino deve ser um número inteiro",
    ):
        AgendaUpdater._validar_anos(
            2026,
            "2027",  # type: ignore[arg-type]
        )


def test_validar_ano_origem_menor_que_um() -> None:
    """Testa ano de origem abaixo do limite."""
    with pytest.raises(
        ValueError,
        match="entre 1 e 9999",
    ):
        AgendaUpdater._validar_anos(
            0,
            2027,
        )


def test_validar_ano_origem_maior_que_9999() -> None:
    """Testa ano de origem acima do limite."""
    with pytest.raises(
        ValueError,
        match="entre 1 e 9999",
    ):
        AgendaUpdater._validar_anos(
            10000,
            2027,
        )


def test_validar_ano_destino_menor_que_um() -> None:
    """Testa ano de destino abaixo do limite."""
    with pytest.raises(
        ValueError,
        match="entre 1 e 9999",
    ):
        AgendaUpdater._validar_anos(
            2026,
            0,
        )


def test_validar_ano_destino_maior_que_9999() -> None:
    """Testa ano de destino acima do limite."""
    with pytest.raises(
        ValueError,
        match="entre 1 e 9999",
    ):
        AgendaUpdater._validar_anos(
            2026,
            10000,
        )


def test_validar_anos_iguais() -> None:
    """Testa bloqueio de anos iguais."""
    with pytest.raises(
        ValueError,
        match="não podem ser iguais",
    ):
        AgendaUpdater._validar_anos(
            2026,
            2026,
        )


def test_atualizar_agenda_arquivo_inexistente(
    tmp_path: Path,
) -> None:
    """Testa atualização com arquivo inexistente."""
    arquivo = tmp_path / "inexistente.docx"
    destino = tmp_path / "resultado.docx"

    updater = criar_updater_mockado()

    with pytest.raises(FileNotFoundError):
        updater.atualizar_agenda(
            arquivo,
            {},
            destino,
        )

    updater.backup_service.criar_backup.assert_not_called()


def test_atualizar_ano_arquivo_inexistente(
    tmp_path: Path,
) -> None:
    """Testa atualização de ano com arquivo inexistente."""
    arquivo = tmp_path / "inexistente.docx"
    destino = tmp_path / "resultado.docx"

    updater = criar_updater_mockado()

    with pytest.raises(FileNotFoundError):
        updater.atualizar_ano(
            arquivo,
            2026,
            2027,
            destino,
        )

    updater.backup_service.criar_backup.assert_not_called()