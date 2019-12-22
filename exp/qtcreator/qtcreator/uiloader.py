import sys

from PySide2.QtCore import QFile, Slot
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QPushButton, QLineEdit

from exp.db import Session
from exp.db.model import Bank



def klik():
    print("Klik")

    bank = Bank(name=edit.text(), active=True)
    sess = Session()
    sess.add(bank)
    sess.commit()

    button.setEnabled(False)
    edit.setText('Haha')



def klik2():
    print("klik2")
    sess = Session()
    print(sess.query(Bank).all())


if __name__ == "__main__":

    # Create db during first run
    # from exp.db import engine, Base
    # from exp.db.model import Bank
    #
    # Base.metadata.create_all(engine)


    app = QApplication(sys.argv)

    ui_file = QFile("bank.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    window.show()
    button: QPushButton = window.findChild(QPushButton, 'pushButton')
    buttonSel: QPushButton = window.findChild(QPushButton, 'pushButtonSelect')
    edit: QLineEdit = window.findChild(QLineEdit, 'lineEdit')
    # button.setEnabled(False)
    button.clicked.connect(klik)
    buttonSel.clicked.connect(klik2)
    sys.exit(app.exec_())
