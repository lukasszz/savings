from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QDialog, QCheckBox, QLineEdit

from db import Session
from db.model import Budget
from form.BudgetEdUi import Ui_Dialog


class BudgetEd(QDialog, Ui_Dialog):

    def __init__(self, obj_id=None, *args, **kwargs):

        super(BudgetEd, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.obj_id = obj_id

        if self.obj_id is not None:
            session = Session()
            a = session.query(Budget).get(self.obj_id)
            self.name.setText(a.name)
            self.active.setChecked(a.active)
        else:
            self.active.setChecked(True)

        self.accepted.connect(self.accept)

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

        self.close()
