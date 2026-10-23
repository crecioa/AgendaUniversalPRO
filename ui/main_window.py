from __future__ import annotations
import os

from pathlib import Path

from config.settings import APP_VERSION
from config.agenda_config import AgendaConfig
from config.app_config import AppConfig
from services.config_service import ConfigService
from ui.agenda_worker import AgendaWorker

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QCloseEvent, QDesktopServices
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
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class DiretoriosDialog(QDialog):
    """Edita os diretórios persistentes utilizados pelo aplicativo."""

    def __init__(self, config: AppConfig, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Configurações de diretórios")
        self.setMinimumWidth(650)
        self.diretorio_origem: Path | None = None
        self.diretorio_destino: Path | None = None

        layout = QVBoxLayout(self)
        formulario = QFormLayout()
        self.origem_edit = QLineEdit(str(config.diretorio_origem))
        self.destino_edit = QLineEdit(str(config.diretorio_destino))

        linha_origem = QHBoxLayout()
        linha_origem.addWidget(self.origem_edit)
        selecionar_origem = QPushButton("Procurar...")
        selecionar_origem.clicked.connect(self._escolher_origem)
        linha_origem.addWidget(selecionar_origem)
        formulario.addRow("Pasta dos modelos:", linha_origem)

        linha_destino = QHBoxLayout()
        linha_destino.addWidget(self.destino_edit)
        selecionar_destino = QPushButton("Procurar...")
        selecionar_destino.clicked.connect(self._escolher_destino)
        linha_destino.addWidget(selecionar_destino)
        formulario.addRow("Pasta de saída:", linha_destino)
        layout.addLayout(formulario)

        botoes = QHBoxLayout()
        botoes.addStretch()
        cancelar = QPushButton("Cancelar")
        cancelar.clicked.connect(self.reject)
        salvar = QPushButton("Salvar")
        salvar.clicked.connect(self._validar)
        botoes.addWidget(cancelar)
        botoes.addWidget(salvar)
        layout.addLayout(botoes)

    def _escolher_origem(self) -> None:
        pasta = QFileDialog.getExistingDirectory(
            self, "Selecionar pasta dos modelos", self.origem_edit.text()
        )
        if pasta:
            self.origem_edit.setText(pasta)

    def _escolher_destino(self) -> None:
        pasta = QFileDialog.getExistingDirectory(
            self, "Selecionar pasta de saída", self.destino_edit.text()
        )
        if pasta:
            self.destino_edit.setText(pasta)

    def _validar(self) -> None:
        origem_texto = self.origem_edit.text().strip()
        destino_texto = self.destino_edit.text().strip()
        if not origem_texto or not destino_texto:
            QMessageBox.warning(self, "Dados inválidos", "Informe as duas pastas.")
            return
        origem = Path(origem_texto).expanduser()
        destino = Path(destino_texto).expanduser()
        if not origem.is_dir():
            QMessageBox.warning(
                self, "Pasta inválida", "A pasta dos modelos deve existir."
            )
            return
        if destino.exists() and not destino.is_dir():
            QMessageBox.warning(
                self, "Destino inválido", "O destino existe, mas não é uma pasta."
            )
            return
        if not destino.exists():
            resposta = QMessageBox.question(
                self,
                "Criar pasta",
                f"A pasta de saída não existe:\n{destino}\n\nDeseja criá-la?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if resposta != QMessageBox.StandardButton.Yes:
                return
            try:
                destino.mkdir(parents=True, exist_ok=True)
            except OSError as erro:
                QMessageBox.critical(self, "Erro ao criar pasta", str(erro))
                return
        self.diretorio_origem = origem
        self.diretorio_destino = destino
        self.accept()


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

        self.worker: AgendaWorker | None = None

        self._resultado_quantidade: int | None = None
        self._resultado_erro: str | None = None
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
        cartao.setObjectName("cartao_atualizacao")

        cartao.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        cartao.setStyleSheet(
            """
            QFrame#cartao_atualizacao {
                border: 1px solid #cccccc;
                border-radius: 10px;
            }
            """
        )

        layout_cartao = QVBoxLayout(cartao)

        layout_cartao.setContentsMargins(
            20, 20, 20, 20
        )

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

        self.botao_nova = QPushButton(
            "Selecionar documento Word"
        )

        self.botao_nova.setMinimumHeight(45)

        self.botao_nova.clicked.connect(
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
            self.botao_nova
        )
        self.barra_progresso = QProgressBar()
        self.barra_progresso.setRange(0, 0)
        self.barra_progresso.setTextVisible(False)
        self.barra_progresso.setMinimumHeight(12)
        self.barra_progresso.hide()

        layout_cartao.addWidget(
            self.barra_progresso
        )
        self.status_processamento = QLabel(
            "Aguardando atualização."
        )
        self.status_processamento.setWordWrap(True)
        self.status_processamento.setStyleSheet(
            """
            QLabel {
                font-size: 12px;
                color: #64748b;
                border: none;
            }
            """
        )

        layout_cartao.addWidget(
            self.status_processamento
        )
        self.painel_resultado = QFrame()
        self.painel_resultado.setObjectName(
            "painel_resultado"
        )

        self.painel_resultado.setStyleSheet(
            """
            QFrame#painel_resultado {
                background-color: #f0fdf4;
                border: 1px solid #bbf7d0;
                border-radius: 8px;
            }
            """
        )

        layout_resultado = QVBoxLayout(
            self.painel_resultado
        )
        layout_resultado.setContentsMargins(15, 15, 15, 15)
        layout_resultado.setSpacing(10)

        titulo_resultado = QLabel(
            "Resultado da última atualização"
        )

        titulo_resultado.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            """
        )

        self.resultado_quantidade = QLabel(
            "Datas atualizadas: 0"
        )

        self.resultado_arquivo = QLabel(
            "Arquivo gerado: —"
        )

        self.resultado_arquivo.setWordWrap(True)

        layout_resultado.addWidget(
            titulo_resultado
        )

        layout_resultado.addWidget(
            self.resultado_quantidade
        )

        layout_resultado.addWidget(
            self.resultado_arquivo
        )

        self.botao_abrir_documento = QPushButton(
            "Abrir documento gerado"
        )

        self.botao_abrir_documento.setObjectName(
            "botao_abrir_documento"
        )

        self.botao_abrir_documento.setMinimumHeight(38)

        self.botao_abrir_documento.setEnabled(False)

        self.botao_abrir_documento.clicked.connect(
            self._abrir_documento_gerado
        )

        layout_resultado.addWidget(
            self.botao_abrir_documento
        )

        self.painel_resultado.hide()

        layout_cartao.addWidget(
            self.painel_resultado
        )

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(descricao)
        layout_principal.addSpacing(20)
        layout_principal.addWidget(cartao)
        layout_principal.addStretch()

        rodape = QLabel(
            f"Agenda Universal PRO — versão {APP_VERSION}"
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

        area_rolagem = QScrollArea()
        area_rolagem.setWidgetResizable(True)
        area_rolagem.setFrameShape(QFrame.Shape.NoFrame)
        area_rolagem.setWidget(central)

        self.setCentralWidget(area_rolagem)
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

        try:
            config = ConfigService().carregar()
            diretorio_origem = config.diretorio_origem

            pasta_inicial = (
                str(diretorio_origem)
                if diretorio_origem.is_dir()
                else ""
            )

        except (OSError, ValueError):
            pasta_inicial = ""

        arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar documento Word",
            pasta_inicial,
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

        if self.worker is not None:
            QMessageBox.warning(
                self,
                "Atualização em andamento",
                "Aguarde a conclusão da atualização atual.",
            )
            return

        config = AgendaConfig(
            arquivo_origem=self.arquivo_origem,
            arquivo_destino=self.arquivo_destino,
            ano_origem=self.ano_origem,
            ano_destino=self.ano_destino,
        )
        self._resultado_quantidade = None
        self._resultado_erro = None

        self.painel_resultado.hide()
        self.botao_abrir_documento.setEnabled(False)

        self.worker = AgendaWorker(config)

        self.worker.sucesso.connect(
            self._atualizacao_concluida
        )
        self.worker.erro.connect(
            self._atualizacao_erro
        )
        self.worker.finished.connect(
            self._atualizacao_finalizada
        )

        self.botao_nova.setEnabled(False)
        self.barra_progresso.show()

        self.status_processamento.setText(
            "Processando documento Word..."
        )

        self.statusBar().showMessage(
            "Atualizando agenda em segundo plano..."
        )

        self.worker.start()

    def _atualizacao_concluida(self, quantidade: int) -> None:
        """Armazena o resultado do processamento."""
        self._resultado_quantidade = quantidade
        self._resultado_erro = None

    def _atualizacao_erro(self, mensagem: str) -> None:
        """Armazena a mensagem de erro."""
        self._resultado_quantidade = None
        self._resultado_erro = mensagem

    def _atualizacao_finalizada(self) -> None:
        """Finaliza a thread e apresenta o resultado."""

        worker = self.worker

        if worker is None:
            return

        # O sinal finished indica que run() terminou.
        # Aguarda o encerramento completo da thread.
        worker.wait()

        self.worker = None
        self.botao_nova.setEnabled(True)
        self.barra_progresso.hide()

        if self._resultado_erro is not None:
            mensagem = self._resultado_erro
            self._resultado_erro = None
            self.status_processamento.setText(
                "Erro durante a atualização."
            )

            self.statusBar().showMessage(
                "Erro durante a atualização."
            )

            QMessageBox.critical(
                self,
                "Erro na atualização",
                (
                    "Não foi possível atualizar "
                    "a agenda.\n\n"
                    f"{mensagem}"
                ),
            )
            return

        quantidade = self._resultado_quantidade
        self._resultado_quantidade = None

        if quantidade is None:
            self.status_processamento.setText(
                "Atualização encerrada sem resultado."
            )

            self.statusBar().showMessage(
                "Atualização encerrada sem resultado."
            )
            return

        self.status_processamento.setText(
            "Atualização concluída com sucesso."
        )

        self.resultado_quantidade.setText(
            f"Datas atualizadas: {quantidade}"
        )

        self.resultado_arquivo.setText(
            f"Arquivo gerado: {self.arquivo_destino}"
        )

        self.botao_abrir_documento.setEnabled(True)
        self.painel_resultado.show()

        self.statusBar().showMessage(
            "Atualização concluída com sucesso."
        )

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

    def _abrir_documento_gerado(self) -> None:
        """Abre o documento gerado no aplicativo padrão do Windows."""
        caminho = self.arquivo_destino

        if caminho is None or not caminho.is_file():
            QMessageBox.warning(
                self,
                "Arquivo não encontrado",
                "O documento gerado não foi encontrado.",
            )
            return

        try:
            os.startfile(str(caminho.resolve()))
        except OSError as erro:
            QMessageBox.warning(
                self,
                "Não foi possível abrir",
                f"Não foi possível abrir o documento Word.\n\n{erro}",
            )

    def closeEvent(self, event: QCloseEvent) -> None:
        """Impede o fechamento durante uma atualização."""

        if self.worker is not None:
            if self.worker.isRunning():
                QMessageBox.warning(
                    self,
                    "Atualização em andamento",
                    (
                        "Aguarde a conclusão da atualização "
                        "antes de fechar o aplicativo."
                    ),
                )
                event.ignore()
                return

        event.accept()

    def _mostrar_configuracoes(self) -> None:
        """Exibe as configurações."""

        servico = ConfigService()
        try:
            atual = servico.carregar()
            dialogo = DiretoriosDialog(atual, self)
            if dialogo.exec() != QDialog.DialogCode.Accepted:
                return
            origem = dialogo.diretorio_origem
            destino = dialogo.diretorio_destino
            if origem is None or destino is None:
                return
            servico.salvar(
                AppConfig(diretorio_origem=origem, diretorio_destino=destino)
            )
        except (OSError, ValueError) as erro:
            QMessageBox.critical(self, "Erro nas configurações", str(erro))
            return
        self.statusBar().showMessage("Configurações salvas com sucesso.")
        QMessageBox.information(
            self, "Configurações", "As pastas foram salvas com sucesso."
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
                f"Versão {APP_VERSION}"
            ),
        )
