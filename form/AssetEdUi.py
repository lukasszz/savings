# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form/AssetEd.ui',
# licensing of 'form/AssetEd.ui' applies.
#
# Created: Sun Apr 19 18:11:49 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name = QtWidgets.QLineEdit(Dialog)
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.currency = QtWidgets.QComboBox(Dialog)
        self.currency.setObjectName("currency")
        self.currency.addItem("")
        self.currency.addItem("")
        self.currency.addItem("")
        self.verticalLayout.addWidget(self.currency)
        self.active = QtWidgets.QCheckBox(Dialog)
        self.active.setObjectName("active")
        self.verticalLayout.addWidget(self.active)
        self.ok_btn = QtWidgets.QDialogButtonBox(Dialog)
        self.ok_btn.setOrientation(QtCore.Qt.Horizontal)
        self.ok_btn.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.ok_btn.setObjectName("ok_btn")
        self.verticalLayout.addWidget(self.ok_btn)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.ok_btn, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.ok_btn, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Asset", None, -1))
        self.name.setText(QtWidgets.QApplication.translate("Dialog", "Name", None, -1))
        self.currency.setItemText(0, QtWidgets.QApplication.translate("Dialog", "PLN", None, -1))
        self.currency.setItemText(1, QtWidgets.QApplication.translate("Dialog", "EUR", None, -1))
        self.currency.setItemText(2, QtWidgets.QApplication.translate("Dialog", "USD", None, -1))
        self.active.setText(QtWidgets.QApplication.translate("Dialog", "Active", None, -1))

