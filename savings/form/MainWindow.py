from datetime import date

from PySide2.QtCore import Qt
from PySide2.QtSql import QSqlTableModel
from PySide2.QtWidgets import QMainWindow, QAction
from sqlalchemy import func, select

from db import Session
from db.model import Transaction, TransactionSplit, Asset, Budget
from form import asset, budget
from form.AssetEd import AssetEd
from form.BudgetEd import BudgetEd
from form.MainWindowUi import Ui_MainWindow
from form.TransferAssetEd import TransferAssetEd
from form.TransferBudgetEd import TransferBudgetEd
from form.TransferIncomeOutcomeEd import TransferIncomeOutcomeEd
from ui.TableModel import TableModel


class MainWindow(QMainWindow, Ui_MainWindow):
    asset_model: QSqlTableModel
    window: QMainWindow

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.setup_asset_table()
        self.setup_budget_table()
        self.setup_transfer_table()

    def act_set_asset_filter(self):
        id_ = self.get_selected_asset()
        idx = self.asset.findData(id_, Qt.UserRole)
        self.asset.setCurrentIndex(idx)

        idx = self.budget.findData(None, Qt.UserRole)
        self.budget.setCurrentIndex(idx)

    def act_set_budget_filter(self):
        id_ = self.get_selected_budget()
        idx = self.budget.findData(id_, Qt.UserRole)
        self.budget.setCurrentIndex(idx)

        idx = self.asset.findData(None, Qt.UserRole)
        self.asset.setCurrentIndex(idx)

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
        self.act_filter()

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
        self.act_filter()

    def setup_transfer_table(self):
        self.dateFrom.setDate(date.today().replace(day=1))

        self.asset.setModel(asset.get_model(with_empty=True))
        self.budget.setModel(budget.get_model(with_empty=True))

        model = TableModel()
        t = Transaction
        s = TransactionSplit
        s = select(
            [t.id, t.date,
             t.desc,
             func.sum(s.amount)
             ]) \
            .select_from(Transaction.__table__.join(s).
                         join(Asset, isouter=True).
                         join(Budget, isouter=True)). \
            group_by(t.id). \
            order_by(t.date.desc(), t.id.desc())
        model.set_sql(s)

        model.add_column_style(4, 'money')
        model.add_column_style(5, 'money')
        self.trans_table.setModel(model)
        self.trans_table.resizeColumnsToContents()

        self.asset.currentIndexChanged.connect(self.act_filter)
        self.budget.currentIndexChanged.connect(self.act_filter)
        self.search.returnPressed.connect(self.act_filter)
        self.dateFrom.dateChanged.connect(self.act_filter)

        self.trans_table.clicked.connect(self.act_show_document)

        act = QAction("Delete", self.trans_table)
        act.triggered.connect(self.act_tran_delete)
        self.trans_table.addAction(act)

    def act_filter(self):
        model: TableModel = self.trans_table.model()

        fa = self.asset.currentData(Qt.UserRole)
        if fa:
            model.sql = model.sql.where(Asset.id == fa)
            model.sql = model.sql.group_by(Asset.id)

        fb = self.budget.currentData(Qt.UserRole)
        if fb:
            model.sql = model.sql.where(Budget.id == fb)
            model.sql = model.sql.group_by(Budget.id)

        fsearch = self.search.text()
        if len(fsearch.strip()):
            model.sql = model.sql.where(Transaction.desc.ilike('%' + fsearch + '%'))

        fdateFrom = self.dateFrom.date().toPython()
        model.sql = model.sql.where(Transaction.date >= fdateFrom)

        model.load_data()
        self.trans_table.resizeColumnsToContents()

    def act_tran_delete(self):
        id_ = self.get_selected_transaction()
        session = Session()
        t = session.query(Transaction).filter(Transaction.id == id_).delete()
        session.commit()
        self.act_filter()
        self.asset_table.model().load_data()
        self.budget_table.model().load_data()

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
        self.asset_table.resizeColumnsToContents()

        # build_menu
        act = QAction("Income/Outcome", self.asset_table)
        act.triggered.connect(self.action_income_outcome_new)
        self.asset_table.addAction(act)
        act = QAction("Transfer", self.asset_table)
        act.triggered.connect(self.act_asset_transfer)
        self.asset_table.addAction(act)
        sep = QAction("", self.asset_table)
        sep.setSeparator(True)
        self.asset_table.addAction(sep)
        act = QAction("New asset", self.asset_table)
        act.triggered.connect(self.act_asset_new)
        self.asset_table.addAction(act)
        act = QAction("Edit asset", self.asset_table)
        act.triggered.connect(self.act_asset_ed)
        self.asset_table.addAction(act)

        self.asset_table.hideColumn(0)

        self.asset_table.doubleClicked.connect(self.action_income_outcome_new)
        self.asset_table.clicked.connect(self.act_set_asset_filter)
        self.asset_table.clicked.connect(self.act_clear_t_ed)

    def act_asset_new(self):
        dlg = AssetEd()
        dlg.exec()
        self.asset_table.model().load_data()

    def act_asset_transfer(self):
        dlg = TransferAssetEd()

        row = self.asset_table.selectedIndexes()
        if len(row) > 0:
            row = row[0].row()
            idx = self.asset_table.model().index(row, 0)
            id_ = self.asset_table.model().data(idx, Qt.UserRole)
            cidx = dlg.from_.findData(id_)
            dlg.from_.setCurrentIndex(cidx)

        dlg.exec()
        self.asset_table.model().load_data()
        self.act_filter()


    def act_asset_ed(self):
        id_ = self.get_selected_asset()
        dlg = AssetEd(id_)
        dlg.exec()
        self.asset_table.model().load_data()

    def get_selected_asset(self):
        row = self.asset_table.selectedIndexes()[0].row()
        idx = self.asset_table.model().index(row, 0)
        id_ = self.asset_table.model().data(idx, Qt.UserRole)
        return id_

    def setup_budget_table(self):
        model = TableModel()
        model.set_sql("SELECT b.id, b.icon, b.name, SUM(coalesce(s.amount, 0.00)) as amount\
                            FROM budget AS b\
                                LEFT OUTER JOIN transaction_split as s ON s.id_budget = b.id\
                            GROUP BY b.id\
                            ORDER BY name")
        model.load_data()
        model.add_column_style(3, 'money')
        model.add_column_style(1, 'icon')
        self.budget_table.setModel(model)
        self.budget_table.resizeColumnsToContents()

        self.budget_table.hideColumn(0)
        # Menu

        act = QAction("Transfer", self.budget_table)
        act.triggered.connect(self.act_budget_transfer)
        self.budget_table.addAction(act)

        sep = QAction("", self.budget_table)
        sep.setSeparator(True)
        self.budget_table.addAction(sep)

        act = QAction("New budget", self.budget_table)
        act.triggered.connect(self.act_budget_new)
        self.budget_table.addAction(act)
        act = QAction("Edit budget", self.budget_table)
        act.triggered.connect(self.act_budget_ed)
        self.budget_table.addAction(act)

        self.budget_table.doubleClicked.connect(self.act_budget_transfer)
        self.budget_table.clicked.connect(self.act_set_budget_filter)
        self.budget_table.clicked.connect(self.act_clear_t_ed)

    def act_budget_new(self):
        dlg = BudgetEd()
        dlg.exec()
        self.budget_table.model().load_data()

    def act_budget_ed(self):
        id_ = self.get_selected_budget()
        dlg = BudgetEd(id_)
        dlg.exec()
        self.budget_table.model().load_data()

    def get_selected_budget(self):
        row = self.budget_table.selectedIndexes()[0].row()
        idx = self.budget_table.model().index(row, 0)
        id_ = self.budget_table.model().data(idx, Qt.UserRole)
        return id_

    def act_show_document(self):
        id_ = self.get_selected_transaction()
        session = Session()
        t = session.query(Transaction).get(id_)
        self.t_ed_id.setText(str(t.id))
        self.t_ed_desc.setText(t.desc)
        self.t_ed_date.setDate(t.date)

        model = TableModel()
        s = TransactionSplit
        model.set_sql(select(
            [Asset.name,
             Budget.icon,
             Budget.name,
             s.amount
             ])
                      .select_from(TransactionSplit.__table__.
                                   join(Asset, isouter=True).
                                   join(Budget, isouter=True)). \
                      where(s.id_transaction == t.id). \
                      order_by(Asset.name, Budget.name))
        model.load_data()
        model.add_column_style(1, 'icon')

        self.t_ed_splits.setModel(model)
        self.t_ed_splits.resizeColumnsToContents()

    def get_selected_transaction(self):
        row = self.trans_table.selectedIndexes()[0].row()
        idx = self.trans_table.model().index(row, 0)
        id_ = self.trans_table.model().data(idx, Qt.UserRole)
        return id_

    def act_clear_t_ed(self):
        self.t_ed_desc.setText('')
        self.t_ed_id.setText('')
        self.t_ed_splits.setModel(TableModel())