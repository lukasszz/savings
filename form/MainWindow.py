import PySide2
import typing

import sqlalchemy
from PySide2.QtCore import qInstallMessageHandler, Qt, QAbstractTableModel
from PySide2.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableView, QPushButton, QCheckBox, QMainWindow, QStyledItemDelegate, \
    QStyleOptionButton, QStyle, QAction
from sqlalchemy import text
from sqlalchemy.orm import session

from db import Session
from form.AssetEd import AssetEd
# // https://stackoverflow.com/questions/11800946/checkbox-and-itemdelegate-in-a-tableview
from form.BudgetEd import BudgetEd
from form.IncomeOutcomeEd import IncomeOutcomeEd


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


class MainWindow:
    asset_model: QSqlTableModel
    window: QMainWindow

    def __init__(self):
        super().__init__()
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("db.sqlite")
        if not db.open():
            print("Cannot open the database")
            exit(1)

        self.window = QUiLoader().load("form/mainwindow.ui")
        # self.setup_asset_list()
        self.budget_table = BudgetList(self.window.findChild(QTableView, 'budget_list'))
        self.asset_table = AssetTable(self.window.findChild(QTableView, 'asset_list'))
        self.io_new: QPushButton = self.window.findChild(QPushButton, 'io_new')
        self.io_new.clicked.connect(
            lambda: self.action_income_outcome_new())

    def action_income_outcome_new(self):
        dlg = IncomeOutcomeEd()

        row = self.asset_table.table.selectedIndexes()
        if len(row) > 0:
            row = row[0].row()
            idx = self.asset_table.model.index(row, 0)
            id_ = self.asset_table.model.data(idx, )
            cidx = dlg.asset.findData(id_)
            dlg.asset.setCurrentIndex(cidx)

        dlg.dialog.exec()
        self.asset_table.model.load_data()
        self.budget_table.model.load_data()


class TableModel(QAbstractTableModel):
    sql: text

    def __init__(self):
        super().__init__()
        self._data = []
        self.sql = None

    def set_sql(self, sql: str):
        self.sql = text(sql)

    def load_data(self):
        sess: session = Session()
        self._data = sess.execute(self.sql).fetchall()
        self.layoutChanged.emit()

    def set_data(self, data):
        self._data = data

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    # def data(self, index:PySide2.QtCore.QModelIndex, role:int=...) -> typing.Any:
    #     pass


class AssetTable:
    def __init__(self, table: QTableView):
        # self.window = window
        self.table = table
        self.model = TableModel()

        self.build_model()
        self.build_menu()
        self.configure_list()

    def build_model(self):
        self.model.set_sql("SELECT a.id, a.name, SUM(coalesce(s.amount, 0.00)) as amount\
                            FROM asset AS a\
                                LEFT OUTER JOIN transaction_split as s ON s.id_asset = a.id\
                            GROUP BY a.id\
                            ORDER BY name")

        self.model.load_data()
        self.table.setModel(self.model)

    def build_menu(self):
        act = QAction("New", self.table)
        act.triggered.connect(self.act_new)
        self.table.addAction(act)
        act = QAction("Edit", self.table)
        act.triggered.connect(self.act_ed)
        self.table.addAction(act)

    def act_new(self):
        dlg = AssetEd()
        dlg.dialog.exec()
        self.model.load_data()

    def act_ed(self):
        row = self.table.selectedIndexes()[0].row()
        idx = self.model.index(row, 0)
        id_ = self.model.data(idx, )
        dlg = AssetEd(id_)
        dlg.dialog.exec()
        self.model.load_data()

    def configure_list(self):
        self.table.hideColumn(0)


class BudgetList:

    def __init__(self, table: QTableView):
        # self.window = window
        self.table = table
        self.model = TableModel()

        self.build_model()
        self.build_menu()
        self.configure_list()

    def build_model(self):
        self.model.set_sql("SELECT b.id, b.name, SUM(coalesce(s.amount, 0.00)) as amount\
                            FROM budget AS b\
                                LEFT OUTER JOIN transaction_split as s ON s.id_budget = b.id\
                            GROUP BY b.id\
                            ORDER BY name")
        self.model.load_data()
        self.table.setModel(self.model)

    def build_menu(self):
        act = QAction("New", self.table)
        act.triggered.connect(self.act_new)
        self.table.addAction(act)
        act = QAction("Edit", self.table)
        act.triggered.connect(self.act_ed)
        self.table.addAction(act)

    def act_new(self):
        dlg = BudgetEd()
        dlg.dialog.exec()
        self.model.load_data()

    def act_ed(self):
        row = self.table.selectedIndexes()[0].row()
        idx = self.model.index(row, 0)
        id_ = self.model.data(idx)
        dlg = BudgetEd(id_)
        dlg.dialog.exec()
        self.model.load_data()

    def configure_list(self):
        self.table.hideColumn(0)
