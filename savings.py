import locale
import sys

from PySide2.QtWidgets import QApplication

import db


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    app = QApplication(sys.argv)

    db.setup('sqlite:///db.sqlite')
    from form.MainWindow import MainWindow
    w = MainWindow()

    w.show()

    sys.exit(app.exec_())
