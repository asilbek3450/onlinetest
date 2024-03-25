import sqlite3


class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                user_id INTEGER
            )
            """
        )

        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY,
                teacher TEXT,
                subject TEXT,
                test_number INTEGER,
                quantity_questions INTEGER,
                all_answers TEXT,
                total_score INTEGER,
                status BOOLEAN
            )
            """
        )

        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS user_test_connection (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                test_id INTEGER,
                sent_answers TEXT,
                correct_answers TEXT,
                total_score INTEGER,
                persentage INTEGER,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (test_id) REFERENCES tests (id),
                unique (user_id, test_id)
            )
            """
        )

        self.conn.commit()

    def delete_table(self, table_name):
        self.cursor.execute(f"DROP TABLE {table_name}")
        self.conn.commit()

    def add_user(self, full_name, user_id):
        self.cursor.execute(
            f"INSERT INTO users (full_name, user_id) VALUES ('{full_name}', {user_id})"
        )
        self.conn.commit()

    def add_test(self, teacher, subject, test_number, quantity_questions, all_answers, total_score, status):
        self.cursor.execute(
            f"INSERT INTO tests (teacher, subject, test_number, quantity_questions, all_answers, total_score, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (teacher, subject, test_number, quantity_questions, all_answers, total_score, status)
        )
        self.conn.commit()

    def add_user_test_connection(self, user_id, test_id, sent_answers, correct_answers, total_score, persentage):
        self.cursor.execute(
            f"INSERT INTO user_test_connection (user_id, test_id, sent_answers, correct_answers, total_score, persentage) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, test_id, sent_answers, correct_answers, total_score, persentage)
        )
        self.conn.commit()

    def get_user_by_id(self, user_id):
        return self.cursor.execute(f"SELECT * FROM users WHERE id = {user_id}").fetchone()

    def get_user_by_user_id(self, user_id):
        return self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()

    def update_user_full_name(self, user_id, full_name):
        self.cursor.execute(f"UPDATE users SET full_name = '{full_name}' WHERE user_id = {user_id}")
        self.conn.commit()

    def get_user_test_connection_by_test_id(self, test_id):
        return self.cursor.execute(f"SELECT * FROM user_test_connection WHERE test_id = {test_id}").fetchall()

    def is_user_test_connection_exists(self, user_id, test_id):
        return self.cursor.execute(f"SELECT * FROM user_test_connection WHERE user_id = {user_id} AND test_id = {test_id}").fetchone()

    def get_test_by_test_number(self, test_number):
        return self.cursor.execute(f"SELECT * FROM tests WHERE test_number = {test_number}").fetchone()

    def update_test_status(self, test_number, status):
        self.cursor.execute(f"UPDATE tests SET status = {status} WHERE test_number = {test_number}")
        self.conn.commit()

    def clear_table(self, table_name):
        self.cursor.execute(f"DELETE FROM {table_name}")
        self.conn.commit()

    def get_current_test_id(self):
        last_id = self.cursor.execute("SELECT id FROM tests ORDER BY id DESC LIMIT 1").fetchone()
        if last_id:
            return last_id[0]
        else:
            return '0'

    def close(self):
        self.conn.close()
