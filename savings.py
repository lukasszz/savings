import sys

from PySide2.QtWidgets import QApplication

from form.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = MainWindow().window

    w.show()

    sys.exit(app.exec_())
