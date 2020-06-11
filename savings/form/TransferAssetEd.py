from datetime import date
from decimal import Decimal

from PySide2.QtGui import Qt
from PySide2.QtWidgets import QDialog

from db import Session
from db.model import Transaction, TransactionSplit
from form import asset
from form.TransferAssetEdUi import Ui_Dialog


class TransferAssetEd(QDialog, Ui_Dialog):

    def __init__(self, obj_id=None, *args, **kwargs):
        super(TransferAssetEd, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.obj_id = obj_id

        self.amount.setFocus()

        if self.obj_id is not None:
            pass
        else:
            pass

        self.from_.setModel(asset.get_model())
        self.to.setModel(asset.get_model())
        self.accepted.connect(self.accept)

    def accept(self):
        t = Transaction()
        t.desc = self.desc.text()
        t.active = True
        t.date = date.today()

        amount = Decimal(self.amount.text().replace(',', '.'))

        split = TransactionSplit()
        split.id_asset = self.from_.currentData(Qt.UserRole)
        split.amount = -amount
        t.splits.append(split)

        split = TransactionSplit()
        split.id_asset = self.to.currentData(Qt.UserRole)
        split.amount = amount
        t.splits.append(split)

        session = Session()
        session.add(t)
        session.commit()

        self.close()


