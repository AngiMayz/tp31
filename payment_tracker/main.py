import sys
from PyQt5.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

def run_app():
    app = QApplication(sys.argv)
    login = LoginWindow()
    if login.exec_() == login.Accepted:
        username = login.username
        window = MainWindow(username)
        window.show()
        window.logout_signal.connect(lambda: restart_app(app)) 
        sys.exit(app.exec_())

def restart_app(app):
    app.quit()
    run_app()

if __name__ == "__main__":
    run_app()