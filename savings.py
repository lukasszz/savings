import sys

import PySide2
from PySide2.QtCore import qInstallMessageHandler
from PySide2.QtSql import QSqlTableModel, QSqlDatabase
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableView, QPushButton, QDialog, QCheckBox, QLineEdit, \
    QMainWindow, QStyledItemDelegate, QStyleOptionButton, QStyle, QAction

from db import Session
from db.model import Asset


# // https://stackoverflow.com/questions/11800946/checkbox-and-itemdelegate-in-a-tableview
class CheckboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        value = index.data()

        opt = QStyleOptionButton()
        if value:
            opt.state = QStyle.State_On
        else:
            opt.state = QStyle.State_Off
        opt.rect = option.rect

        QApplication.style().drawControl(QStyle.CE_CheckBox, opt, painter)

    def createEditor(self, parent: PySide2.QtWidgets.QWidget, option: PySide2.QtWidgets.QStyleOptionViewItem,
                     index: PySide2.QtCore.QModelIndex) -> PySide2.QtWidgets.QWidget:
        return QCheckBox(parent)


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
        self.asset_list: QTableView = self.window.findChild(QTableView, 'asset_table')
        self.asset_list.setModel(self.asset_model)
        self.asset_list.hideColumn(0)
        self.asset_list.setItemDelegateForColumn(2, CheckboxDelegate())
        # self.asset_list.contextMenuEvent = (lambda self.asset_list, event: self.cm

        self.asset_new: QPushButton = self.window.findChild(QPushButton, 'asset_new')
        self.asset_new.clicked.connect(
            lambda: self.action_asset_ed())

        # https://wiki.python.org/moin/PyQt/Handling%20context%20menus
        quitAction = QAction("Quit", self.asset_list)
        quitAction.triggered.connect(lambda: self.cm(self.asset_list))
        self.asset_list.addAction(quitAction)

    def action_asset_ed(self):
        dlg = AssetEd()
        dlg.dialog.exec()
        self.asset_model.select()

    def cm(self, wg):
        print(wg)
        print("Contex menu")


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
