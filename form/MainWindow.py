import PySide2
import typing
from PySide2.QtCore import qInstallMessageHandler, Qt
from PySide2.QtSql import QSqlTableModel, QSqlDatabase, QSqlQueryModel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableView, QPushButton, QCheckBox, QMainWindow, QStyledItemDelegate, \
    QStyleOptionButton, QStyle, QAction

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
            id_ = self.asset_table.model.data(idx)
            cidx = dlg.asset.findData(id_)
            dlg.asset.setCurrentIndex(cidx)

        dlg.dialog.exec()
        self.asset_table.model.setQuery(self.asset_table.model.query())
        self.budget_table.model.setQuery(self.budget_table.model.query())
        self.asset_table.model.query().exec_()
        self.budget_table.model.query().exec_()


# class TableModel(QSqlQueryModel):
#
#     def data(self, item: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
#         if role == Qt.DisplayRole:
#             # value = self.data(item)
            # return 'abc'


class AssetTable:
    def __init__(self, table: QTableView):
        # self.window = window
        self.table = table
        self.model = QSqlQueryModel()

        self.build_model()
        self.build_menu()
        self.configure_list()

    def build_model(self):
        self.model.setQuery("SELECT a.id, a.name, SUM(coalesce(s.amount, 0.00)) as amount\
                            FROM asset AS a\
                                LEFT OUTER JOIN transaction_split as s ON s.id_asset = a.id\
                            GROUP BY a.id\
                            ORDER BY name")
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
        print(self.model.rowCount())
        self.model.query().exec_()
        self.model.setQuery(self.model.query())  # Why I need to this?

    def act_ed(self):
        row = self.table.selectedIndexes()[0].row()
        idx = self.model.index(row, 0)
        id_ = self.model.data(idx)
        dlg = AssetEd(id_)
        dlg.dialog.exec()
        self.model.query().exec_()  # or why I works without setting the query again?

    def configure_list(self):
        self.table.hideColumn(0)


class BudgetList:

    def __init__(self, list_: QTableView):
        # self.window = window
        self.list = list_
        self.model = QSqlQueryModel()

        self.build_model()
        self.build_menu()
        self.configure_list()

    def build_model(self):
        self.model.setQuery("SELECT b.id, b.name, SUM(coalesce(s.amount, 0.00)) as amount\
                            FROM budget AS b\
                                LEFT OUTER JOIN transaction_split as s ON s.id_budget = b.id\
                            GROUP BY b.id\
                            ORDER BY name")
        self.list.setModel(self.model)

    def build_menu(self):
        act = QAction("New", self.list)
        act.triggered.connect(self.act_new)
        self.list.addAction(act)
        act = QAction("Edit", self.list)
        act.triggered.connect(self.act_ed)
        self.list.addAction(act)

    def act_new(self):
        dlg = BudgetEd()
        dlg.dialog.exec()
        print(self.model.rowCount())
        self.model.query().exec_()
        self.model.setQuery(self.model.query())  # Why I need to this?

    def act_ed(self):
        row = self.list.selectedIndexes()[0].row()
        idx = self.model.index(row, 0)
        id_ = self.model.data(idx)
        dlg = BudgetEd(id_)
        dlg.dialog.exec()
        self.model.query().exec_()  # or why I works without setting the query again?

    def configure_list(self):
        self.list.hideColumn(0)
