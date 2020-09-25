import sqlite3

class Member:
    userid: str = ''
    password: str = ''
    phone: str = ''
    email: str = ''
    regdate: str = ''

    def __init__(self):
        self.conn = sqlite3.connect('sqlite.db')

    # C
    def create(self):
        query = "CREATE TABLE IF NOT EXISTS member(userid VARCHAR(10) PRIMARY KEY, passwodr VARCHAR(10), phone VARCHAR(10), regdate DATE DEFAULT CURRENT_TIMESTAMP)"

        self.conn.execute(query)
        self.conn.commit()

    # C
    def insert_many(self):
        data = [
            ('kim', '1', '010-1111-1111'),
            ('lee', '1', '010-2222-2222'),
            ('park', '1', '010-3333-3333')
        ]
        query = "INSERT INTO mamber(userid, password, phone) VALUES (?, ?, ?)"
        

    # R
    def fetch_one(self):
        pass
    
    # R
    def fetch_all(self):
        pass
    
    # R
    def login(self):
        pass
    
    # U
    def update(self):
        pass
    
    # D
    def remove(self):
        pass