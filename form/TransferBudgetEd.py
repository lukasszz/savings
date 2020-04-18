from datetime import date
from decimal import Decimal

from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QComboBox, QLineEdit

from db import Session
from db.model import Budget, Transaction, TransactionSplit
from form import budget


class TransferBudgetEd:
    dialog: QDialog

    def __init__(self, obj_id=None):

        self.obj_id = obj_id
        self.dialog = QUiLoader().load("form/TransferBudgetEd.ui")
        self.from_: QComboBox = self.dialog.findChild(QComboBox, 'from')
        self.to: QComboBox = self.dialog.findChild(QComboBox, 'to')
        self.amount: QLineEdit = self.dialog.findChild(QLineEdit, 'amount')
        self.desc: QLineEdit = self.dialog.findChild(QLineEdit, 'desc')

        self.amount.setFocus()

        if self.obj_id is not None:
            pass
        else:
            pass

        self.from_.setModel(budget.get_model())
        self.to.setModel(budget.get_model())
        self.dialog.accepted.connect(self.accept)

    def accept(self):
        t = Transaction()
        t.desc = self.desc.text()
        t.active = True
        t.date = date.today()

        amount = Decimal(self.amount.text().replace(',', '.'))

        split = TransactionSplit()
        split.id_budget = self.from_.currentData(Qt.UserRole)
        split.amount = -amount
        t.splits.append(split)

        split = TransactionSplit()
        split.id_budget = self.to.currentData(Qt.UserRole)
        split.amount = amount
        t.splits.append(split)

        session = Session()
        session.add(t)
        session.commit()


