import PySide2
from PySide2.QtCore import qInstallMessageHandler
from PySide2.QtSql import QSqlTableModel, QSqlDatabase
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QTableView, QPushButton, QCheckBox, QMainWindow, QStyledItemDelegate, \
    QStyleOptionButton, QStyle, QAction

from form.AssetEd import AssetEd


# // https://stackoverflow.com/questions/11800946/checkbox-and-itemdelegate-in-a-tableview
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
        self.window = QUiLoader().load("form/mainwindow.ui")
        self.setup_asset_list()

    def setup_asset_list(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("db.sqlite")
        if not db.open():
            print("Cannot open the database")
            exit(1)

        self.asset_model = QSqlTableModel(db=db)
        self.asset_model.setTable("asset")
        self.asset_model.setEditStrategy(QSqlTableModel.OnFieldChange)
        # model.setEditStrategy(QSqlTableModel.OnRowChange)
        # model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        self.asset_model.select()

        # noinspection PyTypeChecker
        self.asset_list: QTableView = self.window.findChild(QTableView, 'asset_table')
        self.asset_list.setModel(self.asset_model)
        self.asset_list.setSelectionBehavior(PySide2.QtWidgets.QAbstractItemView.SelectRows)
        self.asset_list.hideColumn(0)
        self.asset_list.setItemDelegateForColumn(2, CheckboxDelegate())

        self.asset_new: QPushButton = self.window.findChild(QPushButton, 'asset_new')
        self.asset_new.clicked.connect(
            lambda: self.action_asset_new())

        # https://wiki.python.org/moin/PyQt/Handling%20context%20menus
        # Menu
        new_act = QAction("New", self.window)
        new_act.triggered.connect(self.action_asset_new)
        self.asset_list.addAction(new_act)

        sep = QAction(self.window)
        sep.setSeparator(True)
        self.asset_list.addAction(sep)

        edit_act = QAction("Edit", self.window)
        edit_act.triggered.connect(self.action_asset_ed)
        self.asset_list.addAction(edit_act)

    def action_asset_new(self):
        dlg = AssetEd()
        dlg.dialog.exec()
        self.asset_model.select()

    def action_asset_ed(self):
        row = self.asset_list.selectedIndexes()[0].row()
        idx = self.asset_model.index(row, 0)
        id = self.asset_model.data(idx)
        print(id)
        dlg = AssetEd(id)
        dlg.dialog.exec()
        self.asset_model.select()
