import sys
import re
import logging
import firebase_admin
from firebase_admin import credentials, db
import bcrypt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QMessageBox, QComboBox, QCheckBox, 
    QScrollArea, QHBoxLayout, QListWidget, 
    QListWidgetItem, QFileDialog
)
from PyQt5.QtCore import Qt

from login_window import LoginWindow
from firebase_manager import FirebaseManager

# Correct Logging Format
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    firebase_manager = FirebaseManager()
    login_window = LoginWindow(firebase_manager)
    login_window.show()
    sys.exit(app.exec_())
