from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QCheckBox, QLineEdit, \
    QComboBox

from db import Session
from db.model import Asset
from form.AssetEdUi import Ui_Dialog


class AssetEd(QDialog, Ui_Dialog):

    def __init__(self, obj_id=None, *args, **kwargs):
        super(AssetEd, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.obj_id = obj_id

        if self.obj_id is not None:
            session = Session()
            a = session.query(Asset).get(self.obj_id)
            self.name.setText(a.name)
            self.active.setChecked(a.active)
            self.currency.setCurrentText(a.currency)
        else:
            self.active.setChecked(True)

        self.accepted.connect(self.accept)

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
        self.close()
