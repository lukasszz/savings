import sys

import PySide2
from PySide2 import QtCore
from PySide2.QtCore import QFile, Slot, Qt, qInstallMessageHandler, QModelIndex
from PySide2.QtSql import QSqlDatabase, QSqlTableModel, QSqlRecord
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QTableView, QAbstractItemDelegate, \
    QStyledItemDelegate, QStyleOptionProgressBar, QStyle, QStyleOption, QStyleOptionButton, QItemDelegate, QCheckBox

from exp.db import Session
from exp.db.model import Bank


def qt_message_handler(mode, context, message):
    if mode == QtCore.QtInfoMsg:
        mode = 'mInfo'
    elif mode == QtCore.QtWarningMsg:
        mode = 'mWarning'
    elif mode == QtCore.QtCriticalMsg:
        mode = 'mcritical'
    elif mode == QtCore.QtFatalMsg:
        mode = 'mfatal'
    else:
        mode = 'Debug'
    print("%s: %s (%s:%d, %s)" % (mode, message, context.file, context.line, context.file))


def get_model():
    model = QSqlTableModel(db=db)
    model.setTable("bank")
    model.setEditStrategy(QSqlTableModel.OnFieldChange)
    # model.setEditStrategy(QSqlTableModel.OnRowChange)
    # model.setEditStrategy(QSqlTableModel.OnManualSubmit)
    model.select()

    # model.removeColumn(0)  # don't show the ID
    # model.setHeaderData(0, Qt.Horizontal, "Name")

    return model


def list1_row_add():
    nr = model1.record()

    # nr.setValue('id', 0)
    nr.setValue('name', 'New..')
    nr.setValue('active', True)

    ok = model1.insertRecord(-1, nr)
    print(db.lastError().text())

    print(ok)
    print(model1.rowCount())
    model1.select()  # With OnFieldChange we need to refresh data to get back the id

    # list1.selectRow(model1.rowCount()-1)
    list1.scrollToBottom()
    idx = list1.model().index(model1.rowCount() - 1, 1, QModelIndex())
    list1.edit(idx)
    # ok = model1.insertRow(-1)
    # print(ok)


def klik():
    print("Klik")


def klik2():
    print("klik2")

# // https://stackoverflow.com/questions/11800946/checkbox-and-itemdelegate-in-a-tableview
class CheckboxDelegate2(QItemDelegate):
    def paint(self, painter: PySide2.QtGui.QPainter, option: PySide2.QtWidgets.QStyleOptionViewItem,
              index: PySide2.QtCore.QModelIndex):

        state = PySide2.QtCore.Qt.CheckState.Checked if index.data() else PySide2.QtCore.Qt.CheckState.Unchecked
        print(option.rect)
        self.drawCheck(painter, option, option.rect, state)
        self.drawFocus(painter, option, option.rect)



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

    def createEditor(self, parent:PySide2.QtWidgets.QWidget, option:PySide2.QtWidgets.QStyleOptionViewItem, index:PySide2.QtCore.QModelIndex) -> PySide2.QtWidgets.QWidget:
        return QCheckBox(parent)


if __name__ == "__main__":
    # Create db during first run
    # from exp.db import engine, Base
    # from exp.db.model import Bank
    #
    # Base.metadata.create_all(engine)

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("../db2.sqlite")
    if not db.open():
        print("Cannot open the database")
        exit(1)

    qInstallMessageHandler(qt_message_handler)
    app = QApplication(sys.argv)

    ui_file = QFile("qtcreator/qtcreator/bank_list.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()
    new1: QPushButton = window.findChild(QPushButton, 'newButton')
    model1 = get_model()
    list1: QTableView = window.findChild(QTableView, 'tableView')
    list1.setModel(model1)
    list1.hideColumn(0)
    list1.setItemDelegateForColumn(2, CheckboxDelegate())
    # button: QPushButton = window.findChild(QPushButton, 'pushButton')
    # buttonSel: QPushButton = window.findChild(QPushButton, 'pushButtonSelect')
    # edit: QLineEdit = window.findChild(QLineEdit, 'lineEdit')
    # # button.setEnabled(False)
    # button.clicked.connect(klik)
    # buttonSel.clicked.connect(klik2)
    new1.clicked.connect(list1_row_add)
    sys.exit(app.exec_())
