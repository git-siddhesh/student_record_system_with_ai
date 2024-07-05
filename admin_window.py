class AdminWindow(QWidget):
    def __init__(self, firebase_manager):
        super().__init__()
        self.firebase_manager = firebase_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Admin Dashboard')
        self.setGeometry(100, 100, 300, 400)
        self.setStyleSheet("background-color: #E3F2FD;")

        self.layout = QVBoxLayout()

        self.title = QLabel('Admin Dashboard', self)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-top: 20px;")
        self.layout.addWidget(self.title)

        self.student_list = QListWidget(self)
        self.student_list.setStyleSheet("font-size: 14px; padding: 8px; margin: 10px; border: 1px solid #ccc; border-radius: 8px; background-color: #fff; color: #333;")
        self.layout.addWidget(self.student_list)

        self.load_students()

        self.logout_button = QPushButton('LOGOUT', self)
        self.logout_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

        self.setLayout(self.layout)

        self.student_list.itemClicked.connect(self.show_student_details)

    def load_students(self):
        students = self.firebase_manager.get_all_students()
        if not students:
            QMessageBox.warning(self, "No Students", "No students found in the database.")
        for i, (username, student) in enumerate(students.items(), 1):
            item = QListWidgetItem(f"{i}. {student['first_name']} {student['last_name']}")
            item.setData(Qt.UserRole, username)
            self.student_list.addItem(item)

    def show_student_details(self, item):
        username = item.data(Qt.UserRole)
        self.student_details_window = DetailedStudentView(self.firebase_manager, username)
        self.student_details_window.show()

    def logout(self):
        self.login_window = LoginWindow(self.firebase_manager)
        self.login_window.show()
        self.close()
