from PySide2.QtGui import QStandardItemModel, QStandardItem, Qt

from db import Session
from db.model import Asset


def get_model(with_empty = False):
    session = Session()
    assets = session.query(Asset).filter(True == Asset.active)

    model = QStandardItemModel()

    if with_empty:
        item = QStandardItem()
        item.setData(-1, Qt.UserRole)
        item.setData('', Qt.DisplayRole)
        model.appendRow(item)

    a: Asset
    for a in assets:
        item = QStandardItem()
        item.setData(a.id, Qt.UserRole)
        item.setData(a.name, Qt.DisplayRole)
        model.appendRow(item)

    return model
