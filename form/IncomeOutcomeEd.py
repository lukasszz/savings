from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QTableView

from db import Session
from db.model import Budget


class BudgetTable:

    def __init__(self, table: QTableView):
        self.table = table
        model = QStandardItemModel(5, 2)
        session = Session()
        budgtes = session.query(Budget).filter(Budget.active == True)
        b: Budget
        i = 0
        for b in budgtes:
            model.setItem(i, 0, QStandardItem(b.name))
            model.setItem(i, 1, QStandardItem('0,00'))
            i += 1
        self.table.setModel(model)


class IncomeOutcomeEd:
    dialog: QDialog

    def __init__(self, obj_id=None):

        self.obj_id = obj_id
        self.dialog = QUiLoader().load("form/income_outcome_ed.ui")
        self.bugets_table: BudgetTable = BudgetTable(self.dialog.findChild(QTableView, 'budget_table'))

        if self.obj_id is not None:
            pass
        else:
            pass
