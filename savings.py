import sys

from PySide2.QtCore import qInstallMessageHandler, QFile
from PySide2.QtSql import QSqlTableModel, QSqlDatabase
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableView, QPushButton, QDialog, QCheckBox, QWidget, QLineEdit, QMainWindow
from PySide2.scripts import uic

from db import Session
from db.model import Asset


class AssetEd:
    dialog: QDialog

    def __init__(self):
        super().__init__()
        self.dialog = QUiLoader().load("form/asset_ed.ui")
        self.name: QLineEdit = self.dialog.findChild(QLineEdit, 'name')
        self.chck: QCheckBox = self.dialog.findChild(QCheckBox, 'active')
        self.chck.setChecked(True)

        self.dialog.accepted.connect(self.accept)

    def accept(self):
        a = Asset(name=self.name.text(), active=True)
        session = Session()
        session.add(a)
        session.commit()


class MainWindow:
    asset_model: QSqlTableModel
    window: QMainWindow

    def __init__(self):
        super().__init__()
        self.window = QUiLoader().load("form/mainwindow.ui")

        self.asset_model = QSqlTableModel(db=db)
        self.asset_model.setTable("asset")
        self.asset_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        # model.setEditStrategy(QSqlTableModel.OnRowChange)
        # model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.asset_model.select()

        # noinspection PyTypeChecker
        self.list1: QTableView = self.window.findChild(QTableView, 'asset_table')
        self.list1.setModel(self.asset_model)
        self.list1.hideColumn(0)

        self.asset_new: QPushButton = self.window.findChild(QPushButton, 'asset_new')
        self.asset_new.clicked.connect(
            lambda: self.action_asset_ed())

    def action_asset_ed(self):
        dlg = AssetEd()
        dlg.dialog.exec()
        self.asset_model.select()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("db.sqlite")
    if not db.open():
        print("Cannot open the database")
        exit(1)

    w = MainWindow().window
    w.show()

    sys.exit(app.exec_())
