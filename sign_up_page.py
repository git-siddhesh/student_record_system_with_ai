class SignupPage(QWidget):
    def __init__(self, firebase_manager):
        super().__init__()
        self.firebase_manager = firebase_manager
        self.login_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register Account")
        self.setGeometry(100, 100, 300, 480)
        self.setStyleSheet("background-color: #E3F2FD;")

        form_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel('Register Account', self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-top: 20px;")

        self.first_name_entry = QLineEdit(self)
        self.first_name_entry.setPlaceholderText('First Name')
        self.first_name_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px;")

        self.last_name_entry = QLineEdit(self)
        self.last_name_entry.setPlaceholderText('Last Name')
        self.last_name_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px;")

        self.email_entry = QLineEdit(self)
        self.email_entry.setPlaceholderText('Email')
        self.email_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px;")

        self.gender_combobox = QComboBox(self)
        self.gender_combobox.addItems(["Male", "Female", "Other"])
        self.gender_combobox.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px;")

        self.role_combobox = QComboBox(self)
        self.role_combobox.addItems(["Student", "Admin", "Super Admin"])
        self.role_combobox.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px;")

        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText('Username')
        self.username_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px;")

        self.login_button = QPushButton('LOGIN', self)
        self.login_button.setStyleSheet("background-color: #2196F3; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.login_button.clicked.connect(self.show_login_page)

        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText('Password')
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.password_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px;")

        self.confirm_password_entry = QLineEdit(self)
        self.confirm_password_entry.setPlaceholderText('Confirm Password')
        self.confirm_password_entry.setEchoMode(QLineEdit.Password)
        self.confirm_password_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px;")

        self.show_password_checkbox = QCheckBox("Show Password", self)
        self.show_password_checkbox.setStyleSheet("margin-left: 20px; font-size: 12px;")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        self.signup_button = QPushButton('REGISTER', self)
        self.signup_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.signup_button.clicked.connect(self.signup)

        layout.addWidget(title)
        layout.addWidget(self.first_name_entry)
        layout.addWidget(self.last_name_entry)
        layout.addWidget(self.email_entry)
        layout.addWidget(self.gender_combobox)
        layout.addWidget(self.role_combobox)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.confirm_password_entry)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.signup_button)
        layout.addWidget(self.login_button)

        form_widget.setLayout(layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(form_widget)

        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def signup(self):
        if not self.validate_inputs():
            return
        if self.firebase_manager.add_user(self.username_entry.text(), self.password_entry.text(), self.first_name_entry.text(),
                                          self.last_name_entry.text(), self.email_entry.text(), self.gender_combobox.currentText(),
                                          self.role_combobox.currentText()):
            QMessageBox.information(self, "Signup Successful", "You have successfully registered!")
            self.show_login_page()
        else:
            QMessageBox.warning(self, "Signup Failed", "Username already exists or an error occurred.")

    def show_login_page(self):
        if self.login_window is not None:
            self.login_window.close()
        self.login_window = LoginWindow(self.firebase_manager)
        self.login_window.show()
        self.close()

    def validate_inputs(self):
        if not all([self.first_name_entry.text(), self.last_name_entry.text(), self.email_entry.text(), self.username_entry.text(),
                    self.password_entry.text(), self.confirm_password_entry.text()]):
            QMessageBox.warning(self, "Signup Failed", "All fields are required.")
            return False
        if self.password_entry.text() != self.confirm_password_entry.text():
            QMessageBox.warning(self, "Signup Failed", "Passwords do not match.")
            return False
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', self.password_entry.text()):
            QMessageBox.warning(self, "Signup Failed", "Password must contain at least one uppercase letter, one numeric digit, and one special character.")
            return False
        return True

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_entry.setEchoMode(QLineEdit.Normal)
            self.confirm_password_entry.setEchoMode(QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QLineEdit.Password)
            self.confirm_password_entry.setEchoMode(QLineEdit.Password)
