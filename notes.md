# Savings 

kurs: https://www.learnpyqt.com/ (75 zł)

https://wiki.qt.io/Technical_FAQ

## 2019-12-26

Autoresize of window: Click right on QDialog in Crator and select the Layout.

https://doc.qt.io/qt-5/layout.html

insertRecord() works with OnManualSubmit()

```sql
model1.select() # With OnFieldChange we need to refresh data to get back the id
```



## 2019-12-24

MV Pattern

https://doc.qt.io/qt-5/modelview.html

Pyside + sqlite model

check drivers

```python
from PySide2.QtSql import QSqlTableModel, QSqlDatabase
QSqlDatabase.drivers()
['QSQLITE', 'QODBC', 'QODBC3', 'QPSQL', 'QPSQL7']
```

Create db object and inspect if we connected to our database:

```python
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("../db2.sqlite")
if not db.open():
    print("Cannot open the database")
    exit(1)
print(db.tables())
print(db.record('bank'))

```



## 2019-12-15

https://doc.qt.io/qtforpython/tutorials/basictutorial/uifiles.html

Installed Qt Creator from fedora app store

## Tutorial

1. Introduction
2. Quick experiment
3. Desgin a db model
4. MVC/MVVM?
5. tests