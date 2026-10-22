from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from config.settings import create_directories
from ui.main_window import MainWindow


def main() -> int:
    """Inicia a interface gráfica do Agenda Universal PRO."""
    create_directories()

    app = QApplication(sys.argv)
    app.setApplicationName("Agenda Universal PRO")
    app.setApplicationVersion("1.1.1")

    janela = MainWindow()
    janela.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
