# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui',
# licensing of 'MainWindow.ui' applies.
#
# Created: Fri Jun 12 17:14:07 2020
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1274, 695)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.budget_table = QtWidgets.QTableView(self.centralwidget)
        self.budget_table.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.budget_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.budget_table.setObjectName("budget_table")
        self.budget_table.horizontalHeader().setVisible(False)
        self.budget_table.horizontalHeader().setStretchLastSection(True)
        self.budget_table.verticalHeader().setVisible(False)
        self.budget_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.budget_table)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.asset_table = QtWidgets.QTableView(self.centralwidget)
        self.asset_table.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.asset_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.asset_table.setObjectName("asset_table")
        self.asset_table.horizontalHeader().setVisible(False)
        self.asset_table.horizontalHeader().setStretchLastSection(True)
        self.asset_table.verticalHeader().setVisible(False)
        self.asset_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.asset_table)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.dateFrom = QtWidgets.QDateEdit(self.centralwidget)
        self.dateFrom.setCalendarPopup(True)
        self.dateFrom.setObjectName("dateFrom")
        self.horizontalLayout_5.addWidget(self.dateFrom)
        self.budget = QtWidgets.QComboBox(self.centralwidget)
        self.budget.setEditable(True)
        self.budget.setObjectName("budget")
        self.horizontalLayout_5.addWidget(self.budget)
        self.asset = QtWidgets.QComboBox(self.centralwidget)
        self.asset.setEditable(True)
        self.asset.setObjectName("asset")
        self.horizontalLayout_5.addWidget(self.asset)
        self.search = QtWidgets.QLineEdit(self.centralwidget)
        self.search.setObjectName("search")
        self.horizontalLayout_5.addWidget(self.search)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.trans_table = QtWidgets.QTableView(self.centralwidget)
        self.trans_table.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.trans_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.trans_table.setSortingEnabled(True)
        self.trans_table.setObjectName("trans_table")
        self.trans_table.horizontalHeader().setVisible(False)
        self.trans_table.horizontalHeader().setStretchLastSection(True)
        self.trans_table.verticalHeader().setVisible(False)
        self.trans_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.trans_table)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.t_ed_id = QtWidgets.QLineEdit(self.centralwidget)
        self.t_ed_id.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.t_ed_id.sizePolicy().hasHeightForWidth())
        self.t_ed_id.setSizePolicy(sizePolicy)
        self.t_ed_id.setObjectName("t_ed_id")
        self.horizontalLayout_4.addWidget(self.t_ed_id)
        self.t_ed_date = QtWidgets.QDateEdit(self.centralwidget)
        self.t_ed_date.setEnabled(False)
        self.t_ed_date.setCalendarPopup(True)
        self.t_ed_date.setObjectName("t_ed_date")
        self.horizontalLayout_4.addWidget(self.t_ed_date)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.t_ed_desc = QtWidgets.QLineEdit(self.centralwidget)
        self.t_ed_desc.setEnabled(False)
        self.t_ed_desc.setObjectName("t_ed_desc")
        self.verticalLayout_4.addWidget(self.t_ed_desc)
        self.t_ed_splits = QtWidgets.QTableView(self.centralwidget)
        self.t_ed_splits.setEnabled(False)
        self.t_ed_splits.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.t_ed_splits.setObjectName("t_ed_splits")
        self.t_ed_splits.horizontalHeader().setVisible(False)
        self.t_ed_splits.horizontalHeader().setStretchLastSection(True)
        self.t_ed_splits.verticalHeader().setVisible(False)
        self.t_ed_splits.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_4.addWidget(self.t_ed_splits)
        self.verticalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_3.setStretch(2, 3)
        self.verticalLayout_3.setStretch(4, 3)
        self.horizontalLayout_6.addLayout(self.verticalLayout_3)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_6.setStretch(2, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Savings", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("MainWindow", "Budgets", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("MainWindow", "Assets", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("MainWindow", "Transactions", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("MainWindow", "Transaction details", None, -1))

