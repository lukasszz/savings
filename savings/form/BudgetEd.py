from PySide2.QtCore import QDirIterator, Qt
from PySide2.QtGui import QIcon, QStandardItem
from PySide2.QtWidgets import QDialog

from db import Session
from db.model import Budget
from form.BudgetEdUi import Ui_Dialog


class BudgetEd(QDialog, Ui_Dialog):

    def __init__(self, obj_id=None, *args, **kwargs):

        super(BudgetEd, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.obj_id = obj_id

        it = QDirIterator(':/icon/icons8/')
        while it.hasNext():
            icon = it.next()
            self.icon.addItem(QIcon(icon), '', icon)

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
        a.icon = self.icon.currentData(Qt.UserRole)

        session.add(a)
        session.commit()

        self.close()
