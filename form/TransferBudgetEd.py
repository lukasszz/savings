from datetime import date
from decimal import Decimal

from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QComboBox, QLineEdit

from db import Session
from db.model import Budget, Transaction, TransactionSplit
from form import budget
from form.TransferBudgetEdUi import Ui_Dialog


class TransferBudgetEd(QDialog, Ui_Dialog):

    def __init__(self, obj_id=None, *args, **kwargs):
        super(TransferBudgetEd, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.obj_id = obj_id

        self.amount.setFocus()

        if self.obj_id is not None:
            pass
        else:
            pass

        self.from_.setModel(budget.get_model())
        self.to.setModel(budget.get_model())
        self.accepted.connect(self.accept)

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

        self.close()


