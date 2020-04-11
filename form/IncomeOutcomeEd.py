from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QTableView, QComboBox

from db import Session
from db.model import Budget, Asset


class BudgetTable:

    def __init__(self, table: QTableView):
        self.table = table
        self.model = QStandardItemModel()

        self.load_budgets_model()
        self.table.setModel(self.model)
        table.hideColumn(0)

    def load_budgets_model(self):
        session = Session()
        budgets = session.query(Budget).filter(True == Budget.active)
        b: Budget
        for b in budgets:
            id = QStandardItem(str(b.id))
            id.setEditable(False)
            name = QStandardItem(b.name)
            name.setEditable(False)
            amount = QStandardItem('0,00')
            amount.setTextAlignment(Qt.AlignRight)
            self.model.appendRow([id, name, amount])


class IncomeOutcomeEd:
    dialog: QDialog

    def __init__(self, obj_id=None):

        self.obj_id = obj_id
        self.dialog = QUiLoader().load("form/income_outcome_ed.ui")
        self.bugets_table: BudgetTable = BudgetTable(self.dialog.findChild(QTableView, 'budget_table'))
        self.asset: QComboBox = self.dialog.findChild(QComboBox, 'asset')

        self.load_asset_model()

        if self.obj_id is not None:
            pass
        else:
            pass

    def load_asset_model(self):
        session = Session()
        assets = session.query(Asset).filter(True == Asset.active)

        model = QStandardItemModel()
        a: Asset
        for a in assets:
            item = QStandardItem()
            item.setData(a.id, Qt.UserRole)
            item.setData(a.name, Qt.DisplayRole)
            model.appendRow(item)

        self.asset.setModel(model)
