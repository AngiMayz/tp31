from PyQt5.QtWidgets import (
    QMainWindow, QTableView, QPushButton, QVBoxLayout, QWidget, QLabel,
    QHBoxLayout, QMessageBox, QDateEdit, QComboBox, QGridLayout, QSpinBox
)
from PyQt5.QtCore import Qt, QSortFilterProxyModel, QDate
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QAbstractItemView, QHeaderView

# Ваши модули
from data_manager import get_payments, add_payment, delete_payment
from report_generator import generate_report
from .add_payment_dialog import AddPaymentDialog
from PyQt5.QtCore import pyqtSignal, QAbstractTableModel


class PaymentTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super(PaymentTableModel, self).__init__()
        self._data = data or []
        self.headers = ["Дата", "Категория", "Назначение", "Количество", "Цена", "Сумма"]

    def rowCount(self, parent=None): return len(self._data)
    def columnCount(self, parent=None): return len(self.headers)

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.headers[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if not index.isValid():
                return None

            row_idx = index.row()
            col_idx = index.column()

            # Проверка выхода за границы
            if row_idx >= len(self._data) or col_idx >= len(self.headers):
                return None

            fields = ["date", "category", "purpose", "quantity", "price", "total"]
            field = fields[col_idx]
            row = self._data[row_idx]

            # Проверяем наличие поля в словаре
            if field not in row:
                return ""

            val = row[field]

            # Обработка числовых полей
            if col_idx in [3, 4, 5]:  # quantity, price, total
                try:
                    val = float(val)
                    if col_idx in [4, 5]:  # price и total
                        return f"{val:.2f} руб."
                    else:  # quantity
                        return str(int(val))
                except (ValueError, TypeError):
                    return "Ошибка"

            # Остальные поля — просто строка
            return str(val)
        return None

class MainWindow(QMainWindow):
    logout_signal = pyqtSignal()  # <-- сигнал для выхода

    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"Учет платежей — {username}")
        self.username = username
        self.payments = get_payments(username)
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        layout = QVBoxLayout()

        # Верхняя панель фильтров
        filter_layout = QGridLayout()

        plus_btn = QPushButton("+")
        minus_btn = QPushButton("-")
        filter_layout.addWidget(plus_btn, 0, 0)
        filter_layout.addWidget(minus_btn, 0, 1)

        start_date_label = QLabel("C")
        end_date_label = QLabel("по")
        self.start_date_edit = QDateEdit(QDate.currentDate())
        self.end_date_edit = QDateEdit(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit.setCalendarPopup(True)
        filter_layout.addWidget(start_date_label, 0, 2)
        filter_layout.addWidget(self.start_date_edit, 0, 3)
        filter_layout.addWidget(end_date_label, 0, 4)
        filter_layout.addWidget(self.end_date_edit, 0, 5)

        category_label = QLabel("Категория:")
        self.category_combo = QComboBox()
        self.category_combo.addItems(["-", "Продукты", "Транспорт", "Развлечения", "Здоровье"])
        filter_layout.addWidget(category_label, 0, 6)
        filter_layout.addWidget(self.category_combo, 0, 7)

        # Кнопки: Выбрать, Очистить, Отчет
        select_btn = QPushButton("Выбрать")
        clear_btn = QPushButton("Очистить")
        report_btn = QPushButton("Отчет")

        filter_layout.addWidget(select_btn, 0, 8)
        filter_layout.addWidget(clear_btn, 0, 9)
        filter_layout.addWidget(report_btn, 0, 10)

        # ---- Таблица ----
        self.table = QTableView()
        self.model = PaymentTableModel(self.payments)
        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(self.model)
        self.table.setModel(proxy_model)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)

        # ---- Кнопки "+" и "-" ----
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ Добавить")
        del_btn = QPushButton("- Удалить")
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(del_btn)

        # ---- Спинбокс количества платежей ----
        self.count_spinbox = QSpinBox()
        self.count_spinbox.setMinimum(1)
        self.count_spinbox.setMaximum(100)
        self.count_spinbox.setValue(1)

        btn_layout.addWidget(QLabel("Количество платежей:"))
        btn_layout.addWidget(self.count_spinbox)

        # ---- Общий лэйаут ----
        layout.addLayout(filter_layout)
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)

        # ---- Подключение сигналов ----
        add_btn.clicked.connect(self.add_payment)
        del_btn.clicked.connect(self.delete_payment)
        select_btn.clicked.connect(self.apply_filters)
        clear_btn.clicked.connect(self.clear_filters)
        report_btn.clicked.connect(self.generate_report)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def add_payment(self):
        dialog = AddPaymentDialog(
            count=self.count_spinbox.value(),  # Теперь корректно
            category=self.category_combo.currentText(),
            parent=self
        )
        if dialog.exec_():
            category = dialog.category_input.text()
            purpose = dialog.purpose_input.text()
            quantity = int(dialog.quantity_input.text())
            price = float(dialog.price_input.text())
            count = dialog.count_input.value()  # Получаем значение из спинбокса

            from data_manager import add_payment
            add_payment(self.username, category, purpose, quantity, price, count)
            self.refresh_table()

    def delete_payment(self):
        idx = self.table.currentIndex().row()
        if idx < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления")
            return
        reply = QMessageBox.question(
            self, "Подтверждение",
            f"Удалить платеж: {self.payments[idx]['purpose']}?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            delete_payment(self.username, idx)
            self.refresh_table()

    def refresh_table(self):
        self.payments = get_payments(self.username)
        self.model._data = self.payments
        self.model.layoutChanged.emit()

    def apply_filters(self):
        start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
        end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
        category = self.category_combo.currentText()

        filtered = self.payments

        try:
            filtered = [
                p for p in filtered
                if start_date <= p["date"].split()[0] <= end_date
            ]
        except KeyError:
            pass

        if category != "-":
            filtered = [p for p in filtered if p["category"] == category]

        self.model._data = filtered
        self.model.layoutChanged.emit()

    def clear_filters(self):
        self.start_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setDate(QDate.currentDate())
        self.category_combo.setCurrentIndex(0)
        self.refresh_table()

    def generate_report(self):
        filename = generate_report(self.username, self.payments)
        QMessageBox.information(self, "Отчет", f"Отчет сохранён: {filename}")
        
    