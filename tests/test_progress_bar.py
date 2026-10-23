"""Testes do indicador visual de processamento."""

from __future__ import annotations

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def test_barra_progresso_inicialmente_oculta() -> None:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    janela = MainWindow()

    assert janela.barra_progresso.isHidden()
    assert janela.barra_progresso.minimum() == 0
    assert janela.barra_progresso.maximum() == 0

    janela.close()
def test_barra_progresso_visivel_durante_processamento() -> None:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    janela = MainWindow()
    janela.show()

    try:
        janela.botao_nova.setEnabled(False)
        janela.barra_progresso.show()

        assert janela.barra_progresso.isVisible()
        assert not janela.botao_nova.isEnabled()
    finally:
        janela.close()


def test_barra_progresso_oculta_apos_processamento() -> None:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    janela = MainWindow()
    janela.show()

    try:
        janela.botao_nova.setEnabled(False)
        janela.barra_progresso.show()

        janela.botao_nova.setEnabled(True)
        janela.barra_progresso.hide()

        assert janela.barra_progresso.isHidden()
        assert janela.botao_nova.isEnabled()
    finally:
        janela.close()