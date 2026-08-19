"""
Agenda Universal PRO
Arquivo: core/agenda_updater.py

Responsável por coordenar a atualização da agenda.
"""

from __future__ import annotations

from pathlib import Path

from services.backup_service import BackupService
from services.logger_service import LoggerService
from services.text_updater import TextUpdater
from services.word_service import WordService


class AgendaUpdater:
    """Coordena o processo de atualização da agenda."""

    def __init__(self) -> None:
        self.logger = LoggerService.get_logger()
        self.word_service = WordService()
        self.backup_service = BackupService()
        self.text_updater = TextUpdater()

    def abrir_agenda(self, arquivo: str | Path):
        """
        Cria um backup, abre o documento Word e localiza as datas.

        Args:
            arquivo: Caminho do documento.

        Returns:
            Documento Word aberto.
        """

        caminho = Path(arquivo)

        self.logger.info("Iniciando processamento: %s", caminho.name)

        self.backup_service.criar_backup(caminho)

        documento = self.word_service.abrir_documento(caminho)

        self.logger.info("Documento carregado com sucesso.")

        ocorrencias = self.text_updater.localizar_datas(documento)

        self.logger.info(
            "Processamento concluído. %d parágrafo(s) com datas.",
            len(ocorrencias),
        )

        return documento

    def atualizar_agenda(
        self,
        arquivo: str | Path,
        substituicoes: dict[str, str],
        destino: str | Path,
    ) -> int:
        """
        Atualiza as datas de uma agenda e salva o resultado.

        Args:
            arquivo: Documento Word original.
            substituicoes: Dicionário com as datas a substituir.
            destino: Caminho onde o documento atualizado será salvo.

        Returns:
            Quantidade de substituições realizadas.

        Raises:
            FileNotFoundError:
                Se o arquivo original não existir.
            ValueError:
                Se o destino for igual ao arquivo original.
        """

        caminho = Path(arquivo)
        caminho_destino = Path(destino)

        self._validar_arquivo_origem(caminho)
        self._validar_destino(caminho, caminho_destino)

        self.logger.info(
            "Iniciando atualização da agenda: %s",
            caminho.name,
        )

        self.backup_service.criar_backup(caminho)

        documento = self.word_service.abrir_documento(caminho)

        quantidade = self.text_updater.atualizar_datas(
            documento,
            substituicoes,
        )

        self.word_service.salvar_documento(
            documento,
            caminho_destino,
        )

        self.logger.info(
            "Agenda atualizada com sucesso. %d substituição(ões).",
            quantidade,
        )

        return quantidade

    def atualizar_ano(
        self,
        arquivo: str | Path,
        ano_origem: int,
        ano_destino: int,
        destino: str | Path,
    ) -> int:
        """
        Atualiza automaticamente o ano das datas de uma agenda
        e salva o resultado.

        Args:
            arquivo: Documento Word original.
            ano_origem: Ano das datas que serão atualizadas.
            ano_destino: Novo ano das datas.
            destino: Caminho onde o documento atualizado será salvo.

        Returns:
            Quantidade de datas atualizadas.

        Raises:
            FileNotFoundError:
                Se o arquivo original não existir.
            ValueError:
                Se os anos forem inválidos ou iguais, ou se o
                destino for igual ao arquivo original.
        """

        caminho = Path(arquivo)
        caminho_destino = Path(destino)

        self._validar_arquivo_origem(caminho)
        self._validar_anos(ano_origem, ano_destino)
        self._validar_destino(caminho, caminho_destino)

        self.logger.info(
            "Iniciando atualização automática da agenda: %s",
            caminho.name,
        )

        self.backup_service.criar_backup(caminho)

        documento = self.word_service.abrir_documento(caminho)

        quantidade = self.text_updater.atualizar_ano(
            documento,
            ano_origem,
            ano_destino,
        )

        self.word_service.salvar_documento(
            documento,
            caminho_destino,
        )

        self.logger.info(
            "Agenda atualizada de %d para %d. "
            "%d substituição(ões) realizada(s).",
            ano_origem,
            ano_destino,
            quantidade,
        )

        return quantidade

    @staticmethod
    def _validar_arquivo_origem(caminho: Path) -> None:
        """Valida a existência do documento original."""

        if not caminho.exists():
            raise FileNotFoundError(
                f"Arquivo de origem não encontrado: {caminho}"
            )

        if not caminho.is_file():
            raise ValueError(
                f"O caminho de origem não é um arquivo: {caminho}"
            )

        if caminho.suffix.lower() != ".docx":
            raise ValueError(
                "O arquivo de origem deve possuir extensão .docx."
            )

    @staticmethod
    def _validar_destino(
        origem: Path,
        destino: Path,
    ) -> None:
        """Impede que o arquivo original seja sobrescrito."""

        if origem.resolve() == destino.resolve():
            raise ValueError(
                "O arquivo de destino não pode ser igual ao arquivo original."
            )

        if destino.suffix.lower() != ".docx":
            raise ValueError(
                "O arquivo de destino deve possuir extensão .docx."
            )

    @staticmethod
    def _validar_anos(
        ano_origem: int,
        ano_destino: int,
    ) -> None:
        """Valida os anos utilizados na atualização."""

        if not isinstance(ano_origem, int):
            raise ValueError("O ano de origem deve ser um número inteiro.")

        if not isinstance(ano_destino, int):
            raise ValueError("O ano de destino deve ser um número inteiro.")

        if ano_origem < 1 or ano_origem > 9999:
            raise ValueError("O ano de origem deve estar entre 1 e 9999.")

        if ano_destino < 1 or ano_destino > 9999:
            raise ValueError("O ano de destino deve estar entre 1 e 9999.")

        if ano_origem == ano_destino:
            raise ValueError(
                "O ano de origem e o ano de destino não podem ser iguais."
            )