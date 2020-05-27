import locale
import os
import sys
import platform
from pathlib import Path
from shutil import copyfile

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from alembic import command
from alembic.config import Config

import db


def get_db_url():
    # if developing
    # return 'sqlite:///db.sqlite'
    if 'Windows' == platform.system():
        return 'sqlite:///' + str(Path.home() / '.savings' / 'db.sqlite')
    else:
        return 'sqlite:////' + str(Path.home() / '.savings' / 'db.sqlite')


def first_run():
    application_path = get_app_global_path()

    savdir = Path.home() / '.savings'
    if savdir.exists():
        return
    savdir.mkdir()
    copyfile(str(Path(application_path) / 'db_template.sqlite'), str(savdir / 'db.sqlite'))


def get_app_global_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    elif __file__:
        return os.path.dirname(__file__)


def upgrade_db():

    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('script_location', str(Path(get_app_global_path()) / 'alembic'))
    alembic_cfg.set_main_option('sqlalchemy.url', get_db_url())
    command.upgrade(alembic_cfg, 'head')


if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

    app = QApplication(sys.argv)

    first_run()
    upgrade_db()
    db.setup(get_db_url())

    from form.MainWindow import MainWindow

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
