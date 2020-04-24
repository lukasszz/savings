import locale
import sys

from PySide2.QtWidgets import QApplication

from form.MainWindow import MainWindow

if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    app = QApplication(sys.argv)

    w = MainWindow()

    w.show()

    sys.exit(app.exec_())
