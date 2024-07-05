class ExtracurricularsInputWindow(QWidget):
    def __init__(self, firebase_manager, username):
        super().__init__()
        self.firebase_manager = firebase_manager
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Extracurriculars')
        self.setGeometry(100, 100, 400, 400)
        self.setStyleSheet("background-color: #E3F2FD;")

        self.layout = QVBoxLayout()

        self.label = QLabel('Add your achievements:', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: #333; margin-top: 20px;")
        self.layout.addWidget(self.label)

        self.achievement_entry = QLineEdit(self)
        self.achievement_entry.setPlaceholderText('Achievement')
        self.achievement_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 10px; border: 1px solid #ccc; border-radius: 8px;")
        self.layout.addWidget(self.achievement_entry)

        self.description_entry = QLineEdit(self)
        self.description_entry.setPlaceholderText('Description (max 30 words)')
        self.description_entry.setStyleSheet("font-size: 14px; padding: 8px; margin: 10px; border: 1px solid #ccc; border-radius: 8px;")
        self.layout.addWidget(self.description_entry)

        self.upload_button = QPushButton('Upload PDF', self)
        self.upload_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 10px;")
        self.upload_button.clicked.connect(self.upload_pdf)
        self.layout.addWidget(self.upload_button)

        self.submit_button = QPushButton('Submit', self)
        self.submit_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.submit_button.clicked.connect(self.submit_achievement)
        self.layout.addWidget(self.submit_button)

        self.add_more_button = QPushButton('Add More', self)
        self.add_more_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 10px;")
        self.add_more_button.clicked.connect(self.add_more_achievement)
        self.layout.addWidget(self.add_more_button)

        self.back_button = QPushButton('Back', self)
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; padding: 10px; border-radius: 10px; margin: 20px;")
        self.back_button.clicked.connect(self.go_back)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

        self.pdf_path = None

    def upload_pdf(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select PDF File", "", "PDF Files (*.pdf)")
        if file_path:
            self.pdf_path = file_path
            QMessageBox.information(self, "File Selected", "PDF file selected successfully.")

    def submit_achievement(self):
        achievement = self.achievement_entry.text()
        description = self.description_entry.text()

        if not achievement or not description or not self.pdf_path:
            QMessageBox.warning(self, "Input Error", "Please fill out all fields and upload a PDF file.")
            return

        if len(description.split()) > 30:
            QMessageBox.warning(self, "Input Error", "Description should not exceed 30 words.")
            return

        if self.firebase_manager.save_pdf_to_database(self.pdf_path, self.username, achievement):
            QMessageBox.information(self, "Success", "Achievement added successfully!")
            # Clear the inputs for adding more achievements
            self.achievement_entry.clear()
            self.description_entry.clear()
            self.pdf_path = None
        else:
            QMessageBox.warning(self, "Failure", "Failed to add achievement. Please try again.")

    def add_more_achievement(self):
        self.achievement_entry.clear()
        self.description_entry.clear()
        self.pdf_path = None
        QMessageBox.information(self, "Add More", "You can add another achievement now.")

    def go_back(self):
        self.home_window = HomeWindow(self.firebase_manager, self.username)
        self.home_window.show()
        self.close()
