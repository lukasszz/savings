import locale
import typing
from decimal import Decimal
from typing import Dict, Any
import resources

import PySide2
from PySide2.QtCore import QAbstractTableModel, Qt
from PySide2.QtGui import QColor, QIcon
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

    def set_sql(self, sql):
        if isinstance(sql, str):
            sql = text(sql)
        self._sql = sql
        self.sql = sql

    def load_data(self, limit=None, offset=None):
        sess: session = Session()

        if limit:
            self.sql = self.sql.limit(limit)
            if offset:
                self.sql = self.sql.offset(offset)

        self._data = sess.execute(self.sql).fetchall()
        self.layoutChanged.emit()
        self.sql = self._sql

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
                        and isinstance(value, int) or isinstance(value, float) or isinstance(value, Decimal):
                    return locale.currency(value, grouping=True)
            if value is None:
                return None
            return str(value)
        if role == Qt.DecorationRole:
            if col in self.column_style:
                if 'icon' in self.column_style[index.column()]:
                    return QIcon(':/icon/icons8/icons8-binoculars-500.png')
        if role == Qt.UserRole:
            return self._data[index.row()][index.column()]
        if role == Qt.TextAlignmentRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, Decimal):
                # Align right, vertical middle.
                return int(Qt.AlignRight | Qt.AlignVCenter)
        if role == Qt.TextColorRole:
            value = self._data[index.row()][index.column()]
            if isinstance(value, int) or isinstance(value, float) or isinstance(value, Decimal):
                if (value < 0):
                    return QColor('red')

    def rowCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        return len(self._data)

    def columnCount(self, parent: PySide2.QtCore.QModelIndex = ...) -> int:
        if len(self._data):
            return len(self._data[0])
        return 0

    # def data(self, index:PySide2.QtCore.QModelIndex, role:int=...) -> typing.Any:
    #     pass
