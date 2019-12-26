import sys

from PySide2.QtGui import Qt
from PySide2.QtSql import QSqlTableModel, QSqlDatabase
from PySide2.QtWidgets import QTableView, QApplication, QLineEdit

db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("../db2.sqlite")
if not db.open():
    print("Cannot open the database")
    exit(1)
print(db.tables())
print(db.record('bank'))


app = QApplication()

model = QSqlTableModel(db=db)
model.setTable("bank")
model.setEditStrategy(QSqlTableModel.OnFieldChange)
model.select()
model.removeColumn(0) # don't show the ID
model.setHeaderData(0, Qt.Horizontal, "Name")
# model.setHeaderData(1, Qt.Horizontal, "Salary")

view = QTableView()
view.setModel(model)
view.show()

sys.exit(app.exec_())