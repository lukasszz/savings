# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form/TransferIncomeOutcomeEd.ui',
# licensing of 'form/TransferIncomeOutcomeEd.ui' applies.
#
# Created: Sun Apr 19 20:41:14 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(670, 444)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.asset = QtWidgets.QComboBox(Dialog)
        self.asset.setEditable(True)
        self.asset.setObjectName("asset")
        self.verticalLayout.addWidget(self.asset)
        self.desc = QtWidgets.QLineEdit(Dialog)
        self.desc.setInputMethodHints(QtCore.Qt.ImhNone)
        self.desc.setText("")
        self.desc.setObjectName("desc")
        self.verticalLayout.addWidget(self.desc)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.budget_table = QtWidgets.QTableView(Dialog)
        self.budget_table.setObjectName("budget_table")
        self.verticalLayout.addWidget(self.budget_table)
        self.sum = QtWidgets.QLineEdit(Dialog)
        self.sum.setEnabled(False)
        self.sum.setMinimumSize(QtCore.QSize(460, 0))
        self.sum.setInputMethodHints(QtCore.Qt.ImhPreferNumbers)
        self.sum.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sum.setObjectName("sum")
        self.verticalLayout.addWidget(self.sum)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Income/Outcome", None, -1))
        self.desc.setToolTip(QtWidgets.QApplication.translate("Dialog", "<html><head/><body><p>Description</p></body></html>", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", "For outcome enter minus amount", None, -1))
        self.sum.setText(QtWidgets.QApplication.translate("Dialog", "0,00", None, -1))

