import locale
from datetime import date
from decimal import Decimal

from PySide2.QtCore import Qt
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QTableView, QComboBox, QLineEdit

from db import Session
from db.model import Budget, Asset, Transaction, TransactionSplit


class BudgetTable:

    def __init__(self, table: QTableView):
        self.table = table
        self.model = QStandardItemModel()

        self.load_budgets_model()
        self.table.setModel(self.model)
        table.hideColumn(0)

    def sum_amount(self):
        m = self.model
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
        session = Session()
        budgets = session.query(Budget).filter(True == Budget.active)
        b: Budget
        for b in budgets:
            id = QStandardItem(str(b.id))
            id.setEditable(False)
            name = QStandardItem(b.name)
            name.setEditable(False)
            amount = QStandardItem('')
            amount.setTextAlignment(Qt.AlignRight)
            self.model.appendRow([id, name, amount])


class TransferIncomeOutcomeEd:
    dialog: QDialog

    def __init__(self, obj_id=None):

        self.obj_id = obj_id
        self.dialog = QUiLoader().load("form/TransferIncomeOutcomeEd.ui")
        self.bugets_table: BudgetTable = BudgetTable(self.dialog.findChild(QTableView, 'budget_table'))
        self.asset: QComboBox = self.dialog.findChild(QComboBox, 'asset')
        self.sum_: QLineEdit = self.dialog.findChild(QLineEdit, 'sum')
        self.desc: QLineEdit = self.dialog.findChild(QLineEdit, 'desc')

        self.load_asset_model()

        if self.obj_id is not None:
            pass
        else:
            pass

        self.dialog.accepted.connect(self.accept)
        self.bugets_table.model.dataChanged.connect(self.on_buget_data_changed)

    def on_buget_data_changed(self):
        amount = self.bugets_table.sum_amount()
        self.sum_.setText(locale.currency(amount, grouping=True))

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

    def accept(self):
        t = Transaction()
        t.desc = self.desc.text()
        t.active = True
        t.date = date.today()
        m = self.bugets_table.model
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
