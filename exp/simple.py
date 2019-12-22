import sys
from PySide2.QtWidgets import QDialog, QApplication, QLineEdit, QPushButton, QVBoxLayout


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Bank")

        self.edit = QLineEdit("Bank")
        self.button = QPushButton("Save")

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.button.clicked.connect(self.msg)

    def msg(self):
        print("Bank saved")


if '__main__' == __name__:
    app = QApplication(sys.argv)
    form = Form()
    form.show()

    sys.exit(app.exec_())
