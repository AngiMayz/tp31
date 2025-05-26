from PyQt5.QtWidgets import QDialog, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QLabel, QMessageBox
from auth import get_user_files, create_new_user, load_user_data, check_password

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Выпадающий список + возможность ввода нового логина
        self.user_combo = QComboBox()
        self.user_combo.setEditable(True)  # Разрешаем ввод новых значений
        self.user_combo.addItems(get_user_files())

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Войти")
        register_btn = QPushButton("Зарегистрироваться")

        layout.addWidget(QLabel("Пользователь:"))
        layout.addWidget(self.user_combo)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_btn)
        layout.addWidget(register_btn)

        self.setLayout(layout)

        login_btn.clicked.connect(self.login)
        register_btn.clicked.connect(self.register)

    def login(self):
        username = self.user_combo.currentText()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        try:
            data = load_user_data(username)
            if check_password(password, data["password"]):
                self.accept()
                self.username = username
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль")
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")

    def register(self):
        username = self.user_combo.currentText()
        password = self.password_input.text()
        result, msg = create_new_user(username, password)
        if result:
            self.user_combo.addItem(username)
            QMessageBox.information(self, "Успех", msg)
        else:
            QMessageBox.warning(self, "Ошибка", msg)

    def login(self):
        username = self.user_combo.currentText()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
        try:
            data = load_user_data(username)
            if check_password(password, data["password"]):
                self.accept()
                self.username = username
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный пароль")
        except Exception:
            QMessageBox.warning(self, "Ошибка", "Пользователь не найден")

    def register(self):
        username = self.user_combo.currentText()
        password = self.password_input.text()
        result, msg = create_new_user(username, password)
        if result:
            self.user_combo.addItem(username)
            QMessageBox.information(self, "Успех", msg)
        else:
            QMessageBox.warning(self, "Ошибка", msg)