"""Testes da abertura do documento Word gerado."""

from __future__ import annotations

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def criar_janela() -> MainWindow:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    return MainWindow()


def test_botao_abrir_inicialmente_desabilitado() -> None:
    janela = criar_janela()

    try:
        assert not janela.botao_abrir_documento.isEnabled()
        assert janela.painel_resultado.isHidden()
    finally:
        janela.close()


def test_botao_abrir_habilitado_apos_sucesso() -> None:
    janela = criar_janela()

    try:
        worker_simulado = MagicMock()
        janela.worker = worker_simulado

        janela.arquivo_destino = Path("agenda_2027.docx")
        janela._resultado_quantidade = 5
        janela._resultado_erro = None

        with patch("ui.main_window.QMessageBox.information"):
            janela._atualizacao_finalizada()

        worker_simulado.wait.assert_called_once()

        assert janela.botao_abrir_documento.isEnabled()
        assert not janela.painel_resultado.isHidden()
    finally:
        janela.close()


def test_abrir_documento_existente(tmp_path: Path) -> None:
    janela = criar_janela()

    try:
        documento = tmp_path / "agenda_2027.docx"
        documento.write_bytes(b"documento de teste")
        janela.arquivo_destino = documento

        with patch("ui.main_window.os.startfile") as abrir:
            janela._abrir_documento_gerado()

        abrir.assert_called_once_with(str(documento.resolve()))
    finally:
        janela.close()


def test_abrir_documento_inexistente(tmp_path: Path) -> None:
    janela = criar_janela()

    try:
        janela.arquivo_destino = (
            tmp_path / "arquivo_inexistente.docx"
        )

        with (
            patch(
                "ui.main_window.QMessageBox.warning"
            ) as aviso,
            patch(
                "ui.main_window.QDesktopServices.openUrl"
            ) as abrir,
        ):
            janela._abrir_documento_gerado()

        aviso.assert_called_once()
        abrir.assert_not_called()
    finally:
        janela.close()


def test_falha_ao_abrir_documento(tmp_path: Path) -> None:
    janela = criar_janela()

    try:
        documento = tmp_path / "agenda_2027.docx"
        documento.write_bytes(b"documento de teste")
        janela.arquivo_destino = documento

        with (
            patch(
                "ui.main_window.os.startfile",
                side_effect=OSError("Falha simulada ao abrir arquivo"),
            ) as abrir,
            patch("ui.main_window.QMessageBox.warning") as aviso,
        ):
            janela._abrir_documento_gerado()

        abrir.assert_called_once()
        aviso.assert_called_once()
    finally:
        janela.close()
