class FirebaseManager:
    def __init__(self):
        try:
            service_account_key = "/Users/nakshatrabhandari/Desktop/PyQt/byebye2-495d8-firebase-adminsdk-qj9te-6f75706abb.json"
            database_url = "https://byebye2-495d8-default-rtdb.asia-southeast1.firebasedatabase.app"
            cred = credentials.Certificate(service_account_key)
            firebase_admin.initialize_app(cred, {'databaseURL': database_url})
            self.db_ref = db.reference('users')
            logging.info("Firebase initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize Firebase: {str(e)}")
            raise Exception("Firebase initialization failed")

    def add_user(self, username, password, first_name, last_name, email, gender, role):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user_data = {
            'password': hashed_password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'gender': gender,
            'role': role
        }
        try:
            if self.db_ref.child(username).get() is None:
                self.db_ref.child(username).set(user_data)
                return True
            else:
                return False
        except Exception as e:
            logging.error(f"Failed to add user: {str(e)}")
            return False

    def get_user(self, username):
        try:
            return self.db_ref.child(username).get()
        except Exception as e:
            logging.error(f"Failed to retrieve user: {str(e)}")
            return None

    def update_student_data(self, username, data):
        try:
            self.db_ref.child(username).update(data)
            return True
        except Exception as e:
            logging.error(f"Failed to update student data: {str(e)}")
            return False

    def get_all_students(self):
        try:
            students = self.db_ref.order_by_child('role').equal_to('Student').get()
            logging.debug(f"Fetched students: {students}")
            return students
        except Exception as e:
            logging.error(f"Failed to retrieve students: {str(e)}")
            return {}

    def update_grade_scores(self, username, grade_level, scores):
        try:
            self.db_ref.child(username).child('grades').child(grade_level).set(scores)
            logging.info(f"Updated {grade_level} scores for {username}")
            return True
        except Exception as e:
            logging.error(f"Failed to update {grade_level} scores for {username}: {str(e)}")
            return False

    def get_grade_scores(self, username, grade_level):
        try:
            scores = self.db_ref.child(username).child('grades').child(grade_level).get()
            return scores if scores else {}
        except Exception as e:
            logging.error(f"Failed to retrieve {grade_level} scores for {username}: {str(e)}")
            return {}

    def save_pdf_to_database(self, local_path, username, achievement_title):
        try:
            with open(local_path, "rb") as pdf_file:
                encoded_string = base64.b64encode(pdf_file.read()).decode('utf-8')
            pdf_data = {
            'title': achievement_title,
            'content': encoded_string
        }
            logging.debug(f"Encoded PDF Data: {pdf_data}")
            self.db_ref.child(username).child('achievements').push(pdf_data)
            logging.info("PDF successfully saved to database.")
            return True
        except Exception as e:
            logging.error(f"Failed to save PDF to database: {str(e)}")
            return False

    def get_pdf_from_database(self, username, achievement_id):
        try:
            pdf_data = self.db_ref.child(username).child('achievements').child(achievement_id).get()
            if pdf_data and 'content' in pdf_data:
                decoded_content = base64.b64decode(pdf_data['content'])
                return decoded_content
            else:
                logging.warning("PDF content not found in database.")
                return None
        except Exception as e:
            logging.error(f"Failed to retrieve PDF from database: {str(e)}")
            return None
