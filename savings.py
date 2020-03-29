import sys

from PySide2.QtCore import qInstallMessageHandler, QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

if __name__ == "__main__":
    # Create db during first run
    # from exp.db import engine, Base
    # from exp.db.model import Bank
    #
    # Base.metadata.create_all(engine)

    # db = QSqlDatabase.addDatabase("QSQLITE")
    # db.setDatabaseName("../db2.sqlite")
    # if not db.open():
    #     print("Cannot open the database")
    #     exit(1)

    app = QApplication(sys.argv)

    ui_file = QFile("form/mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()
    # new1: QPushButton = window.findChild(QPushButton, 'newButton')
    # model1 = get_model()
    # list1: QTableView = window.findChild(QTableView, 'tableView')
    # list1.setModel(model1)
    # list1.hideColumn(0)
    # list1.setItemDelegateForColumn(2, CheckboxDelegate())
    # button: QPushButton = window.findChild(QPushButton, 'pushButton')
    # buttonSel: QPushButton = window.findChild(QPushButton, 'pushButtonSelect')
    # edit: QLineEdit = window.findChild(QLineEdit, 'lineEdit')
    # # button.setEnabled(False)
    # button.clicked.connect(klik)
    # buttonSel.clicked.connect(klik2)
    sys.exit(app.exec_())