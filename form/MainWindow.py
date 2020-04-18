import PySide2
from PySide2.QtCore import qInstallMessageHandler, Qt
from PySide2.QtSql import QSqlTableModel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableView, QPushButton, QCheckBox, QMainWindow, QStyledItemDelegate, \
    QStyleOptionButton, QStyle, QAction

from form.AssetEd import AssetEd
# // https://stackoverflow.com/questions/11800946/checkbox-and-itemdelegate-in-a-tableview
from form.BudgetEd import BudgetEd
from form.MainWindowTrans import MainWindowTrans
from form.TransferIncomeOutcomeEd import TransferIncomeOutcomeEd
from form.TransferBudgetEd import TransferBudgetEd
from ui.TableModel import TableModel


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

        self.window = QUiLoader().load("form/MainWindow.ui")
        self.budget_table = BudgetList(self.window.findChild(QTableView, 'budget_list'))
        self.asset_table = AssetTable(self.window.findChild(QTableView, 'asset_list'))
        self.io_new: QPushButton = self.window.findChild(QPushButton, 'io_new')
        self.io_new.clicked.connect(lambda: self.action_income_outcome_new())

        self.asset_table.table.doubleClicked.connect(self.action_income_outcome_new)
        self.budget_table.table.doubleClicked.connect(self.act_budget_transfer)

        transTab = MainWindowTrans(self.window)

    def act_budget_transfer(self):
        dlg = TransferBudgetEd()

        row = self.budget_table.table.selectedIndexes()
        if len(row) > 0:
            row = row[0].row()
            idx = self.budget_table.model.index(row, 0)
            id_ = self.budget_table.model.data(idx, Qt.UserRole)
            cidx = dlg.from_.findData(id_)
            dlg.from_.setCurrentIndex(cidx)

        dlg.dialog.exec()
        self.budget_table.model.load_data()

    def action_income_outcome_new(self):
        dlg = TransferIncomeOutcomeEd()

        row = self.asset_table.table.selectedIndexes()
        if len(row) > 0:
            row = row[0].row()
            idx = self.asset_table.model.index(row, 0)
            id_ = self.asset_table.model.data(idx, Qt.UserRole)
            cidx = dlg.asset.findData(id_)
            dlg.asset.setCurrentIndex(cidx)

        dlg.dialog.exec()
        self.asset_table.model.load_data()
        self.budget_table.model.load_data()


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
        self.model.add_column_style(2, 'money')
        self.model.load_data()
        self.table.setModel(self.model)

    def build_menu(self):
        act = QAction("New asset", self.table)
        act.triggered.connect(self.act_new)
        self.table.addAction(act)
        act = QAction("Edit asset", self.table)
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
        self.model.add_column_style(2, 'money')
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
