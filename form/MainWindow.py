from datetime import date

import PySide2
from PySide2.QtCore import qInstallMessageHandler, Qt
from PySide2.QtSql import QSqlTableModel
from PySide2.QtWidgets import QApplication, QCheckBox, QMainWindow, QStyledItemDelegate, \
    QStyleOptionButton, QStyle, QAction
from sqlalchemy import func, select, text

from db.model import Transaction, TransactionSplit, Asset, Budget
from form import asset, budget
from form.AssetEd import AssetEd
# // https://stackoverflow.com/questions/11800946/checkbox-and-itemdelegate-in-a-tableview
from form.BudgetEd import BudgetEd
from form.MainWindowUi import Ui_MainWindow
from form.TransferBudgetEd import TransferBudgetEd
from form.TransferIncomeOutcomeEd import TransferIncomeOutcomeEd
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


class MainWindow(QMainWindow, Ui_MainWindow):
    asset_model: QSqlTableModel
    window: QMainWindow

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setup_asset_table()
        self.setup_budget_table()
        self.io_new.clicked.connect(lambda: self.action_income_outcome_new())

        self.asset_table.doubleClicked.connect(self.action_income_outcome_new)
        self.budget_table.doubleClicked.connect(self.act_budget_transfer)

        self.tab_trans()

    def act_budget_transfer(self):
        dlg = TransferBudgetEd()

        row = self.budget_table.selectedIndexes()
        if len(row) > 0:
            row = row[0].row()
            idx = self.budget_table.model().index(row, 0)
            id_ = self.budget_table.model().data(idx, Qt.UserRole)
            cidx = dlg.from_.findData(id_)
            dlg.from_.setCurrentIndex(cidx)

        dlg.exec()
        self.budget_table.model().load_data()

    def action_income_outcome_new(self):
        dlg = TransferIncomeOutcomeEd()

        row = self.asset_table.selectedIndexes()
        if len(row) > 0:
            row = row[0].row()
            idx = self.asset_table.model().index(row, 0)
            id_ = self.asset_table.model().data(idx, Qt.UserRole)
            cidx = dlg.asset.findData(id_)
            dlg.asset.setCurrentIndex(cidx)

        dlg.exec()
        self.asset_table.model().load_data()
        self.budget_table.model().load_data()

    def tab_trans(self):
        self.dateFrom.setDate(date.today().replace(day=1))

        self.asset.setModel(asset.get_model(with_empty=True))
        self.budget.setModel(budget.get_model(with_empty=True))

        model = TableModel()
        t = Transaction
        s = TransactionSplit
        s = select(
            [t.id, t.date,
             t.desc,
             Asset.name,
             Budget.name,
             text("SUM(CASE"
                  "  WHEN amount>0 THEN amount "
                  "  ELSE NULL "
                  "END) AS income "),
             text("SUM(CASE"
                  "  WHEN amount<0 THEN amount "
                  "  ELSE NULL "
                  " END) AS outcome "),

             # text("  CASE "
             #      "    WHEN group_concat(asset.name) IS NULL AND SUM(transaction_split.amount) == 0 THEN 'Budget transfer' "
             #      "    WHEN group_concat(budget.name) IS NULL AND SUM(transaction_split.amount) == 0 THEN 'Asset transfer' "
             #      "    WHEN SUM(transaction_split.amount) > 0 THEN 'Income' "
             #      "    WHEN SUM(transaction_split.amount) < 0 THEN 'Outcome' "
             #      "  ELSE '' END AS type ")
             ]) \
            .select_from(Transaction.__table__.join(s).
                         join(Asset, isouter=True).
                         join(Budget, isouter=True)). \
            group_by(s.id). \
            order_by(t.date.desc(), t.id.desc())
        model.set_sql(s)

        model.add_column_style(4, 'money')
        model.add_column_style(5, 'money')
        model.load_data()
        self.trans_table.setModel(model)
        # self.trans_table.hideColumn(0)

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

    def setup_asset_table(self):

        model = TableModel()
        model.set_sql("SELECT a.id, a.name, SUM(coalesce(s.amount, 0.00)) as amount\
                            FROM asset AS a\
                                LEFT OUTER JOIN transaction_split as s ON s.id_asset = a.id\
                            GROUP BY a.id\
                            ORDER BY name")
        model.add_column_style(2, 'money')
        model.load_data()
        self.asset_table.setModel(model)

        # build_menu
        act = QAction("New asset", self.asset_table)
        act.triggered.connect(self.act_asset_new)
        self.asset_table.addAction(act)
        act = QAction("Edit asset", self.asset_table)
        act.triggered.connect(self.act_asset_ed)
        self.asset_table.addAction(act)

        self.asset_table.hideColumn(0)

    def act_asset_new(self):
        dlg = AssetEd()
        dlg.exec()
        self.asset_table.model().load_data()

    def act_asset_ed(self):
        row = self.asset_table.selectedIndexes()[0].row()
        idx = self.asset_table.model().index(row, 0)
        id_ = self.asset_table.model().data(idx, Qt.UserRole)
        dlg = AssetEd(id_)
        dlg.exec()
        self.asset_table.model().load_data()

    def setup_budget_table(self):
        model = TableModel()
        model.set_sql("SELECT b.id, b.name, SUM(coalesce(s.amount, 0.00)) as amount\
                            FROM budget AS b\
                                LEFT OUTER JOIN transaction_split as s ON s.id_budget = b.id\
                            GROUP BY b.id\
                            ORDER BY name")
        model.load_data()
        model.add_column_style(2, 'money')
        self.budget_table.setModel(model)

        self.budget_table.hideColumn(0)
        # Menu
        act = QAction("New budget", self.budget_table)
        act.triggered.connect(self.act_budget_new)
        self.budget_table.addAction(act)
        act = QAction("Edit budget", self.budget_table)
        act.triggered.connect(self.act_budget_ed)
        self.budget_table.addAction(act)

    def act_budget_new(self):
        dlg = BudgetEd()
        dlg.exec()
        self.budget_table.model().load_data()

    def act_budget_ed(self):
        row = self.budget_table.selectedIndexes()[0].row()
        idx = self.budget_table.model().index(row, 0)
        id_ = self.budget_table.model().data(idx, Qt.UserRole)
        dlg = BudgetEd(id_)
        dlg.exec()
        self.budget_table.model().load_data()
