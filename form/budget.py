from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt

from db import Session
from db.model import Budget


def get_model(with_empty=False):
    session = Session()
    assets = session.query(Budget).filter(True == Budget.active)

    model = QStandardItemModel()

    if with_empty:
        item = QStandardItem()
        item.setData(None, Qt.UserRole)
        item.setData('', Qt.DisplayRole)
        model.appendRow(item)

    a: Budget
    for a in assets:
        item = QStandardItem()
        item.setData(a.id, Qt.UserRole)
        item.setData(a.name, Qt.DisplayRole)
        model.appendRow(item)

    return model
