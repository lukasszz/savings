import locale
import os
import sys
import platform
from pathlib import Path
from shutil import copyfile

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication

import db


def first_run():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    savdir = Path.home() / '.savings'
    if savdir.exists():
        return
    savdir.mkdir()
    copyfile(str(Path(application_path) / 'db_template.sqlite'), str(savdir / 'db.sqlite'))


def setup_db():
    if 'Windows' == platform.system():
        db_url = 'sqlite:///' + str(Path.home() / '.savings' / 'db.sqlite')
    else:
        db_url = 'sqlite:////' + str(Path.home() / '.savings' / 'db.sqlite')
    db.setup(db_url)


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

    app = QApplication(sys.argv)

    first_run()
    setup_db()

    from form.MainWindow import MainWindow
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
