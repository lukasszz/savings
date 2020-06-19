# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TransferIncomeOutcomeEd.ui',
# licensing of 'TransferIncomeOutcomeEd.ui' applies.
#
# Created: Fri Jun 19 08:30:10 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(478, 533)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setBaseSize(QtCore.QSize(0, 0))
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
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.budget_table.sizePolicy().hasHeightForWidth())
        self.budget_table.setSizePolicy(sizePolicy)
        self.budget_table.setObjectName("budget_table")
        self.budget_table.horizontalHeader().setStretchLastSection(True)
        self.budget_table.verticalHeader().setStretchLastSection(False)
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

