import sys

from PySide2.QtCore import QFile, Slot, Qt
from PySide2.QtSql import QSqlDatabase, QSqlTableModel
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit, QTableView, QAbstractItemDelegate, \
    QStyledItemDelegate, QStyleOptionProgressBar, QStyle, QStyleOption, QStyleOptionButton
from pyside2uic.properties import QtCore

from exp.db import Session
from exp.db.model import Bank


def get_model():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("../db2.sqlite")
    if not db.open():
        print("Cannot open the database")
        exit(1)

    model = QSqlTableModel(db=db)
    model.setTable("bank")
    model.setEditStrategy(QSqlTableModel.OnFieldChange)
    model.select()
    # model.removeColumn(0)  # don't show the ID
    # model.setHeaderData(0, Qt.Horizontal, "Name")

    return model


def klik():
    print("Klik")


def klik2():
    print("klik2")


class CheboxDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        value = index.data()

        # progressBarOption = QStyleOptionProgressBar()
        # progressBarOption.rect = option.rect
        # progressBarOption.minimum = 0
        # progressBarOption.maximum = 100
        # progressBarOption.progress = progress
        # progressBarOption.text = str(progress)
        # progressBarOption.textVisible = True

        opt = QStyleOptionButton()
        if value:
            opt.state = QStyle.State_On
        else:
            opt.state = QStyle.State_Off
        opt.rect = option.rect


        QApplication.style().drawControl(QStyle.CE_CheckBox, opt, painter)

if __name__ == "__main__":
    # Create db during first run
    # from exp.db import engine, Base
    # from exp.db.model import Bank
    #
    # Base.metadata.create_all(engine)

    app = QApplication(sys.argv)

    ui_file = QFile("qtcreator/qtcreator/bank_list.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()
    list1: QTableView = window.findChild(QTableView, 'tableView')
    list1.setModel(get_model())
    list1.hideColumn(0)
    list1.setItemDelegateForColumn(2, CheboxDelegate())
    # button: QPushButton = window.findChild(QPushButton, 'pushButton')
    # buttonSel: QPushButton = window.findChild(QPushButton, 'pushButtonSelect')
    # edit: QLineEdit = window.findChild(QLineEdit, 'lineEdit')
    # # button.setEnabled(False)
    # button.clicked.connect(klik)
    # buttonSel.clicked.connect(klik2)
    sys.exit(app.exec_())


