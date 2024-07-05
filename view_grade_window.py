
class ViewGradesWindow(QWidget):
    def __init__(self, firebase_manager, username):
        super().__init__()
        self.firebase_manager = firebase_manager
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('View Grades')
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #E3F2FD;")

        self.layout = QVBoxLayout()

        self.label = QLabel('Your Academic Grades:', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-top: 20px;")
        self.layout.addWidget(self.label)

        self.grades_display = QLabel(self)
        self.grades_display.setAlignment(Qt.AlignLeft)
        self.grades_display.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px; border: 1px solid #ccc; border-radius: 8px; background-color: #fff; color: #333;")
        self.layout.addWidget(self.grades_display)

        self.load_grades()

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.back_button.clicked.connect(self.close)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def load_grades(self):
        user_data = self.firebase_manager.get_user(self.username)
        grades = user_data.get('grades', {}) if user_data else {}
        grades_text = self.format_grades(grades)
        self.grades_display.setText(grades_text)

    def format_grades(self, grades):
        if not grades:
            return "No grades available."
        text = ""
        for grade_level, subjects in grades.items():
            text += f"{grade_level}:\n"
            for subject, details in subjects.items():
                if isinstance(details, dict):
                    text += f"  {subject} ({details['level']}): {details['grade']}\n"
                else:
                    text += f"  {subject}: {details}\n"
            text += "\n"
        return text
