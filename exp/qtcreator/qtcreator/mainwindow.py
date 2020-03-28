import sys

from PySide2.QtCore import QFile
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QInputDialog
from PySide2 import QtGui


def bank_klik():
    print('klik')
    ui_file2 = QFile("bank_list.ui")
    ui_file2.open(QFile.ReadOnly)
    loader2 = QUiLoader()
    window2 = loader2.load(ui_file)
    ui_file2.close()
    window2.show()
    window2.raise_()
    window2.activateWindow()
    print('koniec')
    text, result = QInputDialog.getText(window, "I'm a text Input Dialog!",
                                              "What is your favorite programming language?")
    # import os
    # path, _ = QtGui.QFileDialog.getOpenFileName("Open File", os.getcwd())
    #


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file = QFile("mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()

    bank: QPushButton = window.findChild(QPushButton, 'bankButton')
    bank.clicked.connect(bank_klik)
    window.show()

    sys.exit(app.exec_())