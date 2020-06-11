# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TransferBudgetEd.ui',
# licensing of 'TransferBudgetEd.ui' applies.
#
# Created: Thu Jun 11 15:39:28 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(390, 203)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.from_ = QtWidgets.QComboBox(Dialog)
        self.from_.setEditable(True)
        self.from_.setObjectName("from_")
        self.horizontalLayout.addWidget(self.from_)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.amount = QtWidgets.QLineEdit(Dialog)
        self.amount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.amount.setObjectName("amount")
        self.horizontalLayout.addWidget(self.amount)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.to = QtWidgets.QComboBox(Dialog)
        self.to.setEditable(True)
        self.to.setObjectName("to")
        self.horizontalLayout.addWidget(self.to)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.desc = QtWidgets.QLineEdit(Dialog)
        self.desc.setObjectName("desc")
        self.verticalLayout.addWidget(self.desc)
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
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Budget transfer", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Dialog", ">", None, -1))
        self.amount.setText(QtWidgets.QApplication.translate("Dialog", "0", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Dialog", ">", None, -1))
        self.desc.setToolTip(QtWidgets.QApplication.translate("Dialog", "<html><head/><body><p>Description</p></body></html>", None, -1))

