import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMessageBox

from controller.LevelChooseWindowController import LevelChooseWindowController


def init_window():
    app = QApplication(sys.argv)
    main_window = LevelChooseWindowController()

    def exception_hook(type_, value, tb):
        msg = '\n'.join(traceback.format_exception(type_, value, tb))
        QMessageBox.critical(main_window, 'Unhandled top level exception', msg)

    sys.excepthook = exception_hook

    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    init_window()
