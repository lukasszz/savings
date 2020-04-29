import locale
import os
import sys
from pathlib import Path
from shutil import copyfile

from PySide2.QtWidgets import QApplication

import db

# https://blog.kempj.co.uk/2014/10/packaging-python-app-windows/
def first_run():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    savdir = Path.home() / '.savings'
    if savdir.exists():
        return
    savdir.mkdir()
    copyfile(str(Path(application_path) / 'db.sqlite'), str(savdir / 'db.sqlite'))


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    app = QApplication(sys.argv)

    first_run()

    db.setup('sqlite:////' + str(Path.home() / '.savings' / 'db.sqlite'))
    from form.MainWindow import MainWindow

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
