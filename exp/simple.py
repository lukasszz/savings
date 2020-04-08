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

    def contextMenuEvent(self, event):
        print("Menu!")

    def contextMenuEventExt(self, event):
        print("Menu external!")



if '__main__' == __name__:
    app = QApplication(sys.argv)
    form = Form()
    form.contextMenuEvent = form.contextMenuEventExt
    form.show()

    sys.exit(app.exec_())
