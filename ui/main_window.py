from __future__ import annotations

from pathlib import Path

from config.agenda_config import AgendaConfig
from services.agenda_application import AgendaApplication

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ConfiguracaoDialog(QDialog):
    """Janela para configurar uma atualização de agenda."""

    def __init__(
        self,
        arquivo_origem: Path,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.arquivo_origem = arquivo_origem
        self.arquivo_destino: Path | None = None
        self.ano_origem: int | None = None
        self.ano_destino: int | None = None

        self.setWindowTitle("Configurar atualização")
        self.setMinimumWidth(550)

        self._criar_interface()

    def _criar_interface(self) -> None:
        """Cria os componentes da janela."""

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(30, 25, 30, 25)
        layout_principal.setSpacing(18)

        titulo = QLabel("Configurar atualização")
        titulo.setStyleSheet(
            """
            QLabel {
                font-size: 22px;
                font-weight: bold;
            }
            """
        )

        documento = QLabel(
            f"Documento de origem:\n{self.arquivo_origem}"
        )
        documento.setWordWrap(True)
        documento.setStyleSheet(
            """
            QLabel {
                font-size: 13px;
            }
            """
        )

        formulario = QFormLayout()
        formulario.setSpacing(12)

        self.ano_origem_edit = QLineEdit()
        self.ano_origem_edit.setPlaceholderText(
            "Ex.: 2026"
        )

        self.ano_destino_edit = QLineEdit()
        self.ano_destino_edit.setPlaceholderText(
            "Ex.: 2027"
        )

        formulario.addRow(
            "Ano de origem:",
            self.ano_origem_edit,
        )

        formulario.addRow(
            "Ano de destino:",
            self.ano_destino_edit,
        )

        destino_layout = QHBoxLayout()

        self.arquivo_destino_edit = QLineEdit()
        self.arquivo_destino_edit.setPlaceholderText(
            "Selecione o arquivo de destino"
        )

        botao_destino = QPushButton(
            "Selecionar..."
        )
        botao_destino.clicked.connect(
            self._selecionar_destino
        )

        destino_layout.addWidget(
            self.arquivo_destino_edit
        )
        destino_layout.addWidget(botao_destino)

        formulario.addRow(
            "Arquivo de destino:",
            destino_layout,
        )

        botoes = QHBoxLayout()

        botao_cancelar = QPushButton("Cancelar")
        botao_cancelar.clicked.connect(
            self.reject
        )

        botao_continuar = QPushButton("Continuar")
        botao_continuar.clicked.connect(
            self._confirmar
        )

        botoes.addStretch()
        botoes.addWidget(botao_cancelar)
        botoes.addWidget(botao_continuar)

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(documento)
        layout_principal.addSpacing(5)
        layout_principal.addLayout(formulario)
        layout_principal.addSpacing(10)
        layout_principal.addLayout(botoes)

    def _selecionar_destino(self) -> None:
        """Seleciona o arquivo de destino."""

        arquivo, _ = QFileDialog.getSaveFileName(
            self,
            "Selecionar arquivo de destino",
            "",
            "Documentos Word (*.docx)",
        )

        if not arquivo:
            return

        caminho = Path(arquivo)

        if caminho.suffix.lower() != ".docx":
            caminho = caminho.with_suffix(".docx")

        self.arquivo_destino_edit.setText(
            str(caminho)
        )

    def _confirmar(self) -> None:
        """Valida e confirma a configuração."""

        ano_origem_texto = (
            self.ano_origem_edit.text().strip()
        )

        ano_destino_texto = (
            self.ano_destino_edit.text().strip()
        )

        destino_texto = (
            self.arquivo_destino_edit.text().strip()
        )

        try:
            ano_origem = int(ano_origem_texto)
            ano_destino = int(ano_destino_texto)

        except ValueError:
            QMessageBox.warning(
                self,
                "Dados inválidos",
                "Informe anos válidos.",
            )
            return

        if ano_origem < 1900 or ano_origem > 2100:
            QMessageBox.warning(
                self,
                "Ano inválido",
                "O ano de origem deve estar entre "
                "1900 e 2100.",
            )
            return

        if ano_destino < 1900 or ano_destino > 2100:
            QMessageBox.warning(
                self,
                "Ano inválido",
                "O ano de destino deve estar entre "
                "1900 e 2100.",
            )
            return

        if not destino_texto:
            QMessageBox.warning(
                self,
                "Arquivo não informado",
                "Selecione o arquivo de destino.",
            )
            return

        destino = Path(destino_texto)

        if destino.suffix.lower() != ".docx":
            destino = destino.with_suffix(".docx")

        self.ano_origem = ano_origem
        self.ano_destino = ano_destino
        self.arquivo_destino = destino

        self.accept()


class MainWindow(QMainWindow):
    """Janela principal do Agenda Universal PRO."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Agenda Universal PRO")
        self.setMinimumSize(900, 600)

        self.arquivo_origem: Path | None = None
        self.arquivo_destino: Path | None = None
        self.ano_origem: int | None = None
        self.ano_destino: int | None = None

        self._criar_interface()
        self._criar_menus()
        self._criar_barra_status()

    def _criar_interface(self) -> None:
        """Cria a interface principal."""

        central = QWidget()
        layout_principal = QVBoxLayout(central)

        layout_principal.setContentsMargins(
            40,
            30,
            40,
            30,
        )

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
        cartao.setFrameShape(
            QFrame.Shape.StyledPanel
        )

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

        titulo_cartao = QLabel(
            "Nova atualização"
        )

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

        layout_cartao.addWidget(
            titulo_cartao
        )

        layout_cartao.addWidget(
            descricao_cartao
        )

        layout_cartao.addSpacing(10)

        layout_cartao.addWidget(
            self.arquivo_label
        )

        layout_cartao.addWidget(
            botao_nova
        )

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

        self._abrir_configuracao()

    def _abrir_configuracao(self) -> None:
        """Abre a janela de configuração."""

        if self.arquivo_origem is None:
            return

        dialogo = ConfiguracaoDialog(
            self.arquivo_origem,
            self,
        )

        if (
            dialogo.exec()
            != QDialog.DialogCode.Accepted
        ):
            self.statusBar().showMessage(
                "Configuração cancelada."
            )
            return

        self.ano_origem = dialogo.ano_origem
        self.ano_destino = dialogo.ano_destino
        self.arquivo_destino = (
            dialogo.arquivo_destino
        )

        if (
            self.arquivo_destino is None
            or self.ano_origem is None
            or self.ano_destino is None
        ):
            QMessageBox.critical(
                self,
                "Erro de configuração",
                "A configuração da atualização "
                "não foi preenchida corretamente.",
            )

            self.statusBar().showMessage(
                "Erro na configuração."
            )
            return

        config = AgendaConfig(
            arquivo_origem=self.arquivo_origem,
            arquivo_destino=self.arquivo_destino,
            ano_origem=self.ano_origem,
            ano_destino=self.ano_destino,
        )

        aplicacao = AgendaApplication()

        self.statusBar().showMessage(
            "Atualizando agenda..."
        )

        try:
            quantidade = aplicacao.atualizar(
                config
            )

        except Exception as erro:
            QMessageBox.critical(
                self,
                "Erro na atualização",
                (
                    "Não foi possível atualizar "
                    "a agenda.\n\n"
                    f"{erro}"
                ),
            )

            self.statusBar().showMessage(
                "Erro durante a atualização."
            )
            return

        QMessageBox.information(
            self,
            "Atualização concluída",
            (
                "A agenda foi atualizada com sucesso."
                "\n\n"
                f"Datas atualizadas: {quantidade}"
                "\n"
                f"Arquivo gerado:\n"
                f"{self.arquivo_destino}"
            ),
        )

        self.statusBar().showMessage(
            "Atualização concluída com sucesso."
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