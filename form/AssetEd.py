from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QCheckBox, QLineEdit, \
    QComboBox

from db import Session
from db.model import Asset


class AssetEd:
    dialog: QDialog

    def __init__(self, obj_id=None):
        super().__init__()
        self.obj_id = obj_id
        self.dialog = QUiLoader().load("form/asset_ed.ui")
        self.name: QLineEdit = self.dialog.findChild(QLineEdit, 'name')
        self.active: QCheckBox = self.dialog.findChild(QCheckBox, 'active')
        self.currency: QComboBox = self.dialog.findChild(QComboBox, 'currency')

        if self.obj_id is not None:
            session = Session()
            a = session.query(Asset).get(self.obj_id)
            self.name.setText(a.name)
            self.active.setChecked(a.active)
            self.currency.setCurrentText(a.currency)
        else:
            self.active.setChecked(True)

        self.dialog.accepted.connect(self.accept)

    def accept(self):
        session = Session()
        if self.obj_id is not None:
            a: Asset = session.query(Asset).get(self.obj_id)
        else:
            a = Asset()

        a.name = self.name.text()
        a.active = self.active.isChecked()
        a.currency = self.currency.currentText()

        session.add(a)
        session.commit()
