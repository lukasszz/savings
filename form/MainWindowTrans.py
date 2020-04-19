from datetime import date

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QTableView, QComboBox, QDateEdit, QLineEdit
from sqlalchemy import select, func, text

from db.model import Transaction, TransactionSplit, Budget, Asset
from form import asset, budget
from ui.TableModel import TableModel


class MainWindowTrans:
    trans_table: QTableView
    window: QMainWindow

    def __init__(self, window: QMainWindow):
        self.window = window

        self.trans_table: QTableView = self.window.findChild(QTableView, 'trans_table')
        self.budget: QComboBox = self.window.findChild(QComboBox, 'budget')
        self.asset: QComboBox = self.window.findChild(QComboBox, 'asset')
        self.dateFrom: QDateEdit = self.window.findChild(QDateEdit, 'dateFrom')
        self.search: QLineEdit = self.window.findChild(QLineEdit, 'search')

        self.dateFrom.setDate(date.today().replace(day=1))

        self.asset.setModel(asset.get_model(with_empty=True))
        self.budget.setModel(budget.get_model(with_empty=True))

        model = TableModel()
        t = Transaction
        s = TransactionSplit
        s = select(
            [t.id, t.date, t.desc, func.sum(s.amount), func.group_concat(Budget.name), func.group_concat(Asset.name),
             text("  CASE "
                  "    WHEN group_concat(asset.name) IS NULL AND SUM(transaction_split.amount) == 0 THEN 'b>b' "
                  "    WHEN group_concat(budget.name) IS NULL AND SUM(transaction_split.amount) == 0 THEN 'a>a' "
                  "    WHEN SUM(transaction_split.amount) > 0 THEN 'IN' "
                  "    WHEN SUM(transaction_split.amount) < 0 THEN 'OUT' "
                  "  ELSE '' END AS type ")]) \
            .select_from(Transaction.__table__.join(s).
                         join(Asset, isouter=True).
                         join(Budget, isouter=True)). \
            group_by(t.id). \
            order_by(t.date.desc(), t.id.desc())
        model.set_sql(s)

        model.add_column_style(3, 'money')
        model.load_data(10)
        self.trans_table.setModel(model)
        self.trans_table.hideColumn(0)

        self.asset.currentIndexChanged.connect(self.filter)
        self.budget.currentIndexChanged.connect(self.filter)
        self.search.returnPressed.connect(self.filter)
        self.dateFrom.dateChanged.connect(self.filter)

    def filter(self):

        model: TableModel = self.trans_table.model()

        fa = self.asset.currentData(Qt.UserRole)
        if fa:
            model.sql = model.sql.where(Asset.id == fa)

        fb = self.budget.currentData(Qt.UserRole)
        if fb:
            model.sql = model.sql.where(Budget.id == fb)

        fsearch = self.search.text()
        if len(fsearch.strip()):
            model.sql = model.sql.where(Transaction.desc.ilike('%' + fsearch + '%'))

        fdateFrom = self.dateFrom.date().toPython()
        model.sql = model.sql.where(Transaction.date >= fdateFrom)

        model.load_data()
