import locale
from datetime import date
from decimal import Decimal

from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QTableView, QComboBox, QLineEdit

from db import Session
from db.model import Budget, Asset, Transaction, TransactionSplit
from form import asset
from form.TransferIncomeOutcomeEdUi import Ui_Dialog


class TransferIncomeOutcomeEd(QDialog, Ui_Dialog):

    def __init__(self, obj_id=None, *args, **kwargs):
        super(TransferIncomeOutcomeEd, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.obj_id = obj_id

        self.asset.setModel(asset.get_model())

        self.load_budgets_model()
        self.budget_table.hideColumn(0)
        if self.obj_id is not None:
            pass
        else:
            pass

        self.accepted.connect(self.accept)
        self.budget_table.model().dataChanged.connect(self.on_buget_data_changed)

    def sum_amount(self):
        m = self.budget_table.model()
        sum_ = 0
        for idx in range(m.rowCount()):
            amount = m.item(idx, 2).data(0)
            if '' == amount:
                continue
            amount = Decimal(amount.replace(',', '.'))
            if amount == Decimal('0.00'):
                continue
            sum_ += amount
        return sum_

    def load_budgets_model(self):
        model = QStandardItemModel()

        session = Session()
        budgets = session.query(Budget).filter(True == Budget.active).order_by(Budget.name)
        b: Budget
        for b in budgets:
            id = QStandardItem(str(b.id))
            id.setEditable(False)
            name = QStandardItem(b.name)
            name.setEditable(False)
            amount = QStandardItem('')
            amount.setTextAlignment(Qt.AlignRight)
            model.appendRow([id, name, amount])
        self.budget_table.setModel(model)

    def on_buget_data_changed(self):
        amount = self.sum_amount()
        self.sum.setText(locale.currency(amount, grouping=True))

    def accept(self):
        t = Transaction()
        t.desc = self.desc.text()
        t.active = True
        t.date = date.today()
        m = self.budget_table.model()
        for idx in range(m.rowCount()):
            bud_id = m.item(idx, 0).data(0)
            amount = m.item(idx, 2).data(0)
            if '' == amount:
                continue
            amount = Decimal(amount.replace(',', '.'))
            if amount == Decimal('0.00'):
                continue

            split = TransactionSplit()
            split.id_budget = bud_id
            split.id_asset = self.asset.currentData(Qt.UserRole)
            split.amount = amount
            t.splits.append(split)
        session = Session()
        session.add(t)
        session.commit()

        self.close()
