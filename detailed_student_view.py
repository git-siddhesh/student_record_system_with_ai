
class DetailedStudentView(QWidget):
    def __init__(self, firebase_manager, username):
        super().__init__()
        self.firebase_manager = firebase_manager
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Student Details - {self.username}")
        self.setGeometry(100, 100, 400, 600)
        self.setStyleSheet("background-color: #E3F2FD;")

        self.layout = QVBoxLayout()

        student_data = self.firebase_manager.get_user(self.username)

        if student_data:
            self.details_label = QLabel(f"Details for {student_data['first_name']} {student_data['last_name']}", self)
            self.details_label.setAlignment(Qt.AlignCenter)
            self.details_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #333; margin-top: 20px;")
            self.layout.addWidget(self.details_label)

            self.info_label = QLabel(self)
            self.info_label.setStyleSheet("font-size: 14px; padding: 8px; margin: 15px;")
            self.info_label.setText(self.format_student_info(student_data))
            self.layout.addWidget(self.info_label)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.back_button.clicked.connect(self.close)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def format_student_info(self, student_data):
        info = (
            f"First Name: {student_data.get('first_name', 'N/A')}\n"
            f"Last Name: {student_data.get('last_name', 'N/A')}\n"
            f"Email: {student_data.get('email', 'N/A')}\n"
            f"Gender: {student_data.get('gender', 'N/A')}\n"
            f"Role: {student_data.get('role', 'N/A')}\n"
        )

        total_marks_11th = sum(subject['grade'] if isinstance(subject, dict) else subject for subject in student_data.get('grades', {}).get('11th Grade', {}).values())
        total_marks_12th = sum(subject['grade'] if isinstance(subject, dict) else subject for subject in student_data.get('grades', {}).get('12th Grade', {}).values())

        if '11th Grade' in student_data.get('grades', {}):
            info += "\n11th Grade Scores:\n"
            for subject, details in student_data['grades']['11th Grade'].items():
                if isinstance(details, dict):
                    info += f"  {subject} ({details['level']}): {details['grade']}\n"
                else:
                    info += f"  {subject}: {details}\n"
            info += f"Total Marks: {total_marks_11th} / 42\n"

        if '12th Grade' in student_data.get('grades', {}):
            info += "\n12th Grade Scores:\n"
            for subject, details in student_data['grades']['12th Grade'].items():
                if isinstance(details, dict):
                    info += f"  {subject} ({details['level']}): {details['grade']}\n"
                else:
                    info += f"  {subject}: {details}\n"
            info += f"Total Marks: {total_marks_12th} / 42\n"

        if 'SAT Scores' in student_data:
            info += "\nSAT Scores:\n"
            sat_scores = student_data['SAT Scores']
            info += f"  Math: {sat_scores.get('Math', 'N/A')}\n"
            info += f"  English: {sat_scores.get('English', 'N/A')}\n"

        return info
