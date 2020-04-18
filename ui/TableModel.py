import locale
import typing
from typing import Dict, Any

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt
from PySide2.QtGui import QColor
from sqlalchemy import text
from sqlalchemy.orm import session

from db import Session


class TableModel(QAbstractTableModel):
    column_styles: Dict[Any, list]
    sql: text

    def __init__(self):
        super().__init__()
        self._data = []
        self.sql = None
        self.column_style = {}

    def add_column_style(self, index, style):
        if index not in self.column_style:
            self.column_style[index] = []
        self.column_style[index].append(style)

    def set_sql(self, sql: str):
        self.sql = text(sql)

    def load_data(self):
        sess: session = Session()
        self._data = sess.execute(self.sql).fetchall()
        self.layoutChanged.emit()

    def set_data(self, data):
        self._data = data

    def data(self, index: PySide2.QtCore.QModelIndex, role: int = ...) -> typing.Any:
        col = index.column()
        if role == Qt.DisplayRole:
            value = self._data[index.row()][col]
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            if col in self.column_style:
                if 'money' in self.column_style[index.column()] \
                        and isinstance(value, int) or isinstance(value, float):
                    return locale.currency(value, grouping=True)

            return value
        if role == Qt.UserRole:
            return self._data[index.row()][index.column()]
        if role == Qt.TextAlignmentRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, int) or isinstance(value, float):
                # Align right, vertical middle.
                return int(Qt.AlignRight | Qt.AlignVCenter)
        if role == Qt.TextColorRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, int) or isinstance(value, float):
                if (value < 0):
                    return QColor('red')

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    # def data(self, index:PySide2.QtCore.QModelIndex, role:int=...) -> typing.Any:
    #     pass
