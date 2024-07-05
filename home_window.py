class HomeWindow(QWidget):
    def __init__(self, firebase_manager, username):
        super().__init__()
        self.firebase_manager = firebase_manager
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Home Page')
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet("background-color: #E3F2FD;")
        
        welcome_label = QLabel(f'Welcome, {self.username}', self)
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-top: 30px;")

        self.view_details_button = QPushButton('View Details', self)
        self.view_details_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.view_details_button.clicked.connect(self.view_details)

        self.view_grades_button = QPushButton('View Grades', self)
        self.view_grades_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.view_grades_button.clicked.connect(self.view_grades)

        self.extracurriculars_button = QPushButton('Extracurriculars', self)
        self.extracurriculars_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.extracurriculars_button.clicked.connect(self.open_extracurriculars)

        self.logout_button = QPushButton('LOGOUT', self)
        self.logout_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.logout_button.clicked.connect(self.logout)

        layout = QVBoxLayout()
        layout.addWidget(welcome_label)
        layout.addWidget(self.view_details_button)
        layout.addWidget(self.view_grades_button)
        layout.addWidget(self.extracurriculars_button)
        layout.addWidget(self.logout_button)
        self.setLayout(layout)

    def view_details(self):
        self.details_window = StudentDetailsWindow(self.firebase_manager, self.username)
        self.details_window.show()

    def view_grades(self):
        self.grades_window = ViewGradesWindow(self.firebase_manager, self.username)
        self.grades_window.show()

    def open_extracurriculars(self):
        self.extracurriculars_window = ExtracurricularsInputWindow(self.firebase_manager, self.username)
        self.extracurriculars_window.show()
        self.close()

    def logout(self):
        self.login_window = LoginWindow(self.firebase_manager)
        self.login_window.show()
        self.close()
