class LoginWindow(QWidget):
    def __init__(self, firebase_manager):
        super().__init__()
        self.firebase_manager = firebase_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Login Page')
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet("background-color: #E3F2FD;")

        title = QLabel("AJEETA MA'AM", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-top: 30px;")

        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText('Enter Username')
        self.username_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 20px; border: 1px solid #ccc; border-radius: 8px;")

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText('Enter password')
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 20px; border: 1px solid #ccc; border-radius: 8px;")

        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("margin-left: 20px; font-size: 12px;")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        self.login_button = QPushButton('LOGIN', self)
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.login_button.clicked.connect(self.login)

        register_button = QPushButton("REGISTER", self)
        register_button.clicked.connect(self.open_register_page)
        register_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.login_button)
        layout.addWidget(register_button)
        self.setLayout(layout)

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if not username or not password:
            QMessageBox.warning(self, "Login Failed", "Both email and password fields must be filled out.")
            return

        user_data = self.firebase_manager.get_user(username)
        if user_data and bcrypt.checkpw(password.encode(), user_data['password'].encode()):
            if user_data['role'] == 'Student':
                self.open_home_page(username)
            elif user_data['role'] == 'Admin':
                self.open_admin_window()
            else:
                self.open_home_page(username)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")

    def open_home_page(self, username):
        self.home_window = HomeWindow(self.firebase_manager, username)
        self.home_window.show()
        self.close()

    def open_admin_window(self):
        self.admin_window = AdminWindow(self.firebase_manager)
        self.admin_window.show()
        self.close()

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)

    def open_register_page(self):
        self.registration_page = SignupPage(self.firebase_manager)
        self.registration_page.show()
        self.close()
