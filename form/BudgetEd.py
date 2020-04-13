from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QCheckBox, QLineEdit, \
    QComboBox

from db import Session
from db.model import Asset, Budget


class BudgetEd:
    dialog: QDialog

    def __init__(self, obj_id=None):
        super().__init__()
        self.obj_id = obj_id
        self.dialog = QUiLoader().load("form/budget_ed.ui")
        self.name: QLineEdit = self.dialog.findChild(QLineEdit, 'name')
        self.active: QCheckBox = self.dialog.findChild(QCheckBox, 'active')

        if self.obj_id is not None:
            session = Session()
            a = session.query(Budget).get(self.obj_id)
            self.name.setText(a.name)
            self.active.setChecked(a.active)
        else:
            self.active.setChecked(True)

        self.dialog.accepted.connect(self.accept)

    def accept(self):
        session = Session()
        if self.obj_id is not None:
            a: Budget = session.query(Budget).get(self.obj_id)
        else:
            a = Budget()

        a.name = self.name.text()
        a.active = self.active.isChecked()

        session.add(a)
        session.commit()
