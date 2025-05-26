from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QSpinBox

class AddPaymentDialog(QDialog):
    def __init__(self, count, category, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить платеж")
        self.count = count     # Это целое число
        self.category = category  # Это строка
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.category_input = QLineEdit(self.category)  # Передаём строку
        self.purpose_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.price_input = QLineEdit()

        self.count_input = QSpinBox()
        self.count_input.setMinimum(1)
        self.count_input.setMaximum(100)
        self.count_input.setValue(self.count)  # Теперь это число!

        layout.addWidget(QLabel("Категория:"))
        layout.addWidget(self.category_input)
        layout.addWidget(QLabel("Назначение (не менее 3 букв):"))
        layout.addWidget(self.purpose_input)
        layout.addWidget(QLabel("Количество:"))
        layout.addWidget(self.quantity_input)
        layout.addWidget(QLabel("Цена (руб.):"))
        layout.addWidget(self.price_input)
        layout.addWidget(QLabel("Сколько раз добавить:"))
        layout.addWidget(self.count_input)

        submit = QPushButton("Добавить")
        submit.clicked.connect(self.validate_and_accept)
        layout.addWidget(submit)

        self.setLayout(layout)
    def add_payment(self):
        dialog = AddPaymentDialog(
            count=self.count_spinbox.value(),  # Теперь self.count_spinbox существует
            category=self.category_combo.currentText(),
            parent=self
        )
        if dialog.exec_():
            category = dialog.category_input.text()
            purpose = dialog.purpose_input.text()
            quantity = int(dialog.quantity_input.text())
            price = float(dialog.price_input.text())
            count = dialog.count_input.value()

            from data_manager import add_payment
            add_payment(self.username, category, purpose, quantity, price, count)
            self.refresh_table() 
            
    def validate_and_accept(self):
        category = self.category_input.text().strip()
        purpose = self.purpose_input.text().strip()
        quantity = self.quantity_input.text().strip()
        price = self.price_input.text().strip()

        if not purpose or len(purpose) < 3:
            QMessageBox.warning(self, "Ошибка", "Назначение должно быть не менее 3 букв")
            return
        if not quantity.isdigit() or int(quantity) <= 0:
            QMessageBox.warning(self, "Ошибка", "Количество должно быть положительным числом")
            return
        if not price.replace('.', '', 1).isdigit() or float(price) < 0:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть неотрицательным числом")
            return

        self.accept()