from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    """Janela principal do Agenda Universal PRO."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Agenda Universal PRO")
        self.setMinimumSize(900, 600)

        self.arquivo_origem: Path | None = None

        self._criar_interface()
        self._criar_menus()
        self._criar_barra_status()

    def _criar_interface(self) -> None:
        """Cria a interface principal."""

        central = QWidget()
        layout_principal = QVBoxLayout(central)

        layout_principal.setContentsMargins(40, 30, 40, 30)
        layout_principal.setSpacing(20)

        titulo = QLabel("Agenda Universal PRO")
        titulo.setStyleSheet(
            """
            QLabel {
                font-size: 30px;
                font-weight: bold;
            }
            """
        )
        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        descricao = QLabel(
            "Atualização e gerenciamento de agendas."
        )
        descricao.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
            }
            """
        )
        descricao.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        cartao = QFrame()
        cartao.setFrameShape(QFrame.Shape.StyledPanel)
        cartao.setStyleSheet(
            """
            QFrame {
                border: 1px solid #cccccc;
                border-radius: 10px;
                padding: 20px;
            }
            """
        )

        layout_cartao = QVBoxLayout(cartao)
        layout_cartao.setSpacing(12)

        titulo_cartao = QLabel("Nova atualização")
        titulo_cartao.setStyleSheet(
            """
            QLabel {
                font-size: 20px;
                font-weight: bold;
                border: none;
            }
            """
        )

        descricao_cartao = QLabel(
            "Selecione uma agenda Word para iniciar."
        )
        descricao_cartao.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                border: none;
            }
            """
        )

        self.arquivo_label = QLabel(
            "Nenhum documento selecionado."
        )
        self.arquivo_label.setWordWrap(True)
        self.arquivo_label.setStyleSheet(
            """
            QLabel {
                font-size: 13px;
                border: none;
            }
            """
        )

        botao_nova = QPushButton(
            "Selecionar documento Word"
        )
        botao_nova.setMinimumHeight(45)
        botao_nova.clicked.connect(
            self._nova_atualizacao
        )

        layout_cartao.addWidget(titulo_cartao)
        layout_cartao.addWidget(descricao_cartao)
        layout_cartao.addSpacing(10)
        layout_cartao.addWidget(self.arquivo_label)
        layout_cartao.addWidget(botao_nova)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descricao)
        layout_principal.addSpacing(20)
        layout_principal.addWidget(cartao)
        layout_principal.addStretch()

        rodape = QLabel(
            "Agenda Universal PRO — versão 1.0.0"
        )
        rodape.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        rodape.setStyleSheet(
            """
            QLabel {
                font-size: 12px;
            }
            """
        )

        layout_principal.addWidget(rodape)

        self.setCentralWidget(central)

    def _criar_menus(self) -> None:
        """Cria os menus da aplicação."""

        menu_arquivo = self.menuBar().addMenu(
            "Arquivo"
        )

        menu_agenda = self.menuBar().addMenu(
            "Agenda"
        )

        menu_configuracoes = self.menuBar().addMenu(
            "Configurações"
        )

        menu_ajuda = self.menuBar().addMenu(
            "Ajuda"
        )

        acao_nova = QAction(
            "Nova atualização",
            self,
        )
        acao_nova.triggered.connect(
            self._nova_atualizacao
        )

        acao_sair = QAction(
            "Sair",
            self,
        )
        acao_sair.triggered.connect(
            self.close
        )

        acao_configuracoes = QAction(
            "Configurações",
            self,
        )
        acao_configuracoes.triggered.connect(
            self._mostrar_configuracoes
        )

        acao_sobre = QAction(
            "Sobre",
            self,
        )
        acao_sobre.triggered.connect(
            self._mostrar_sobre
        )

        menu_arquivo.addAction(acao_sair)
        menu_agenda.addAction(acao_nova)
        menu_configuracoes.addAction(
            acao_configuracoes
        )
        menu_ajuda.addAction(acao_sobre)

    def _criar_barra_status(self) -> None:
        """Cria a barra de status."""

        self.statusBar().showMessage(
            "Pronto para iniciar."
        )

    def _nova_atualizacao(self) -> None:
        """Seleciona o documento Word de origem."""

        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar documento Word",
            "",
            "Documentos Word (*.docx)",
        )

        if not arquivo:
            self.statusBar().showMessage(
                "Seleção cancelada."
            )
            return

        self.arquivo_origem = Path(arquivo)

        self.arquivo_label.setText(
            f"Documento selecionado:\n"
            f"{self.arquivo_origem}"
        )

        self.statusBar().showMessage(
            "Documento selecionado com sucesso."
        )

    def _mostrar_configuracoes(self) -> None:
        """Exibe as configurações."""

        QMessageBox.information(
            self,
            "Configurações",
            "A tela de configurações será "
            "implementada em uma próxima etapa.",
        )

    def _mostrar_sobre(self) -> None:
        """Exibe informações da aplicação."""

        QMessageBox.about(
            self,
            "Sobre o Agenda Universal PRO",
            (
                "<b>Agenda Universal PRO</b><br><br>"
                "Sistema para atualização e "
                "gerenciamento de agendas.<br><br>"
                "Versão 1.0.0"
            ),
        )