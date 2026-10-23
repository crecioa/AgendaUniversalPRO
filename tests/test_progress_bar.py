"""Testes do indicador visual de processamento."""

from __future__ import annotations
from unittest.mock import MagicMock, patch

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
def test_status_processamento_inicial() -> None:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    janela = MainWindow()

    try:
        assert (
            janela.status_processamento.text()
            == "Aguardando atualização."
        )
    finally:
        janela.close()


def test_status_processamento_durante_atualizacao() -> None:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    janela = MainWindow()

    try:
        janela.status_processamento.setText(
            "Processando documento Word..."
        )

        assert (
            janela.status_processamento.text()
            == "Processando documento Word..."
        )
    finally:
        janela.close()


def test_status_processamento_apos_sucesso() -> None:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    janela = MainWindow()

    try:
        janela.status_processamento.setText(
            "Atualização concluída com sucesso."
        )

        assert (
            janela.status_processamento.text()
            == "Atualização concluída com sucesso."
        )
    finally:
        janela.close()
def test_status_atualizado_apos_conclusao_do_worker() -> None:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    janela = MainWindow()

    try:
        worker_simulado = MagicMock()
        janela.worker = worker_simulado

        janela._resultado_quantidade = 5
        janela._resultado_erro = None

        janela.botao_nova.setEnabled(False)
        janela.barra_progresso.show()

        janela.status_processamento.setText(
            "Processando documento Word..."
        )

        with patch(
            "ui.main_window.QMessageBox.information"
        ):
            janela._atualizacao_finalizada()

        worker_simulado.wait.assert_called_once()

        assert janela.worker is None
        assert janela.botao_nova.isEnabled()
        assert janela.barra_progresso.isHidden()

        assert (
            janela.status_processamento.text()
            == "Atualização concluída com sucesso."
        )

    finally:
        janela.close()
def test_status_atualizado_apos_erro_do_worker() -> None:
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    janela = MainWindow()

    try:
        worker_simulado = MagicMock()
        janela.worker = worker_simulado

        janela._resultado_quantidade = None
        janela._resultado_erro = "Erro simulado de processamento"

        janela.botao_nova.setEnabled(False)
        janela.barra_progresso.show()

        janela.status_processamento.setText(
            "Processando documento Word..."
        )

        with patch(
            "ui.main_window.QMessageBox.critical"
        ) as mensagem_erro:
            janela._atualizacao_finalizada()

        worker_simulado.wait.assert_called_once()

        assert janela.worker is None
        assert janela.botao_nova.isEnabled()
        assert janela.barra_progresso.isHidden()

        assert (
            janela.status_processamento.text()
            == "Erro durante a atualização."
        )

        assert janela._resultado_erro is None
        mensagem_erro.assert_called_once()

    finally:
        janela.close()