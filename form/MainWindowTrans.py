from datetime import date

from PySide2.QtWidgets import QMainWindow, QTableView, QComboBox, QDateEdit

from form import asset, budget
from ui.TableModel import TableModel


class MainWindowTrans:
    trans_table: QTableView
    window: QMainWindow

    def __init__(self, window: QMainWindow):
        self.window = window

        self.trans_table: QTableView = self.window.findChild(QTableView, 'trans_table')
        self.budget: QComboBox = self.window.findChild(QComboBox, 'budget')
        self.asset: QComboBox = self.window.findChild(QComboBox, 'asset')
        self.dateFrom: QDateEdit = self.window.findChild(QDateEdit, 'dateFrom')

        self.dateFrom.setDate(date.today().replace(day=1))

        self.asset.setModel(asset.get_model(with_empty=True))
        self.budget.setModel(budget.get_model(with_empty=True))


        model = TableModel()
        model.set_sql("SELECT t.id, t.date, t.desc, SUM(s.amount) AS amount, "
                      "  group_concat(b.name), group_concat(a.name), "
                      "  CASE "
                      "    WHEN group_concat(a.name) IS NULL AND SUM(s.amount) == 0 THEN 'b>b' "
                      "    WHEN group_concat(b.name) IS NULL AND SUM(s.amount) == 0 THEN 'a>a' "
                      "    WHEN SUM(s.amount) > 0 THEN 'IN' "
                      "    WHEN SUM(s.amount) < 0 THEN 'OUT' "
                      "  ELSE '' END AS type "
                      "FROM 'transaction' AS t "
                      "  JOIN transaction_split AS s ON s.id_transaction = t.id "
                      "  LEFT OUTER JOIN budget AS b ON b.id = s.id_budget "
                      "  LEFT OUTER JOIN asset AS a ON a.id = s.id_asset "
                      "GROUP BY t.id "
                      "ORDER by t.date DESC, t.id DESC")
        model.add_column_style(3, 'money')
        model.load_data()
        self.trans_table.setModel(model)
        self.trans_table.hideColumn(0)
