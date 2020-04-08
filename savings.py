import sys

import PySide2
from PySide2.QtCore import qInstallMessageHandler
from PySide2.QtSql import QSqlTableModel, QSqlDatabase
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableView, QPushButton, QDialog, QCheckBox, QLineEdit, \
    QMainWindow, QStyledItemDelegate, QStyleOptionButton, QStyle, QAction, QMenu, QComboBox

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

    def __init__(self, obj_id=None):
        super().__init__()
        self.obj_id = obj_id
        self.dialog = QUiLoader().load("form/asset_ed.ui")
        self.name: QLineEdit = self.dialog.findChild(QLineEdit, 'name')
        self.active: QCheckBox = self.dialog.findChild(QCheckBox, 'active')
        self.currency: QComboBox = self.dialog.findChild(QComboBox, 'currency')

        if self.obj_id is not None:
            session = Session()
            a = session.query(Asset).get(self.obj_id)
            self.name.setText(a.name)
            self.active.setChecked(a.active)
            self.currency.setCurrentText(a.currency)
        else:
            self.active.setChecked(True)

        self.dialog.accepted.connect(self.accept)

    def accept(self):
        session = Session()
        if self.obj_id is not None:
            a: Asset = session.query(Asset).get(self.obj_id)
            a.name = self.name.text()
            a.active = self.active.isChecked()
            a.currency = self.currency.currentText()
        else:
            a = Asset(name=self.name.text(), active=True)
        session.add(a)
        session.commit()


class MainWindow:
    asset_model: QSqlTableModel
    window: QMainWindow

    def __init__(self):
        super().__init__()
        self.window = QUiLoader().load("form/mainwindow.ui")
        self.setup_asset_list()

    def setup_asset_list(self):
        self.asset_model = QSqlTableModel(db=db)
        self.asset_model.setTable("asset")
        self.asset_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        # model.setEditStrategy(QSqlTableModel.OnRowChange)
        # model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.asset_model.select()

        # noinspection PyTypeChecker
        self.asset_list: QTableView = self.window.findChild(QTableView, 'asset_table')
        self.asset_list.setModel(self.asset_model)
        self.asset_list.setSelectionBehavior(PySide2.QtWidgets.QAbstractItemView.SelectRows)
        self.asset_list.hideColumn(0)
        self.asset_list.setItemDelegateForColumn(2, CheckboxDelegate())

        self.asset_new: QPushButton = self.window.findChild(QPushButton, 'asset_new')
        self.asset_new.clicked.connect(
            lambda: self.action_asset_new())

        # https://wiki.python.org/moin/PyQt/Handling%20context%20menus
        # Menu
        edit_act = QAction("Edit", self.window)
        edit_act.triggered.connect(self.action_asset_ed)
        self.asset_list.addAction(edit_act)

        sep = QAction(self.window)
        sep.setSeparator(True)

        self.asset_list.addAction(sep)
        abc = QAction("Del", self.window)
        self.asset_list.addAction(abc)

    def action_asset_new(self):
        dlg = AssetEd()
        dlg.dialog.exec()
        self.asset_model.select()

    def action_asset_ed(self):
        row = self.asset_list.selectedIndexes()[0].row()
        idx = self.asset_model.index(row, 0)
        id = self.asset_model.data(idx)
        print(id)
        dlg = AssetEd(id)
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
