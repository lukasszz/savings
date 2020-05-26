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
    # db_url = 'sqlite:///db.sqlite'
    db.setup(db_url)


def upgrade_db():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('script_location', str(Path(application_path) / 'alembic'))
    db_url = 'sqlite:////' + str(Path.home() / '.savings' / 'db.sqlite')
    alembic_cfg.set_main_option('sqlalchemy.url', db_url)
    command.upgrade(alembic_cfg, 'head')
    # import alembic.config
    # alembicArgs = [
    #     '--raiseerr',
    #     'upgrade', 'head',
    # ]
    # alembic.config.main(argv=alembicArgs)



if __name__ == "__main__":
    locale.setlocale(locale.LC_ALL, '')
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

    app = QApplication(sys.argv)

    first_run()
    print('run')
    upgrade_db()
    print('upgrade')
    setup_db()

    from form.MainWindow import MainWindow
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
