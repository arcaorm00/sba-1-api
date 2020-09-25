import sqlite3

class Member:
    id: str = ''
    pwd: str = ''
    name: str = ''
    birth: str = ''
    regdate: str = ''

    def __init__(self):
        self.conn = sqlite3.connect('sqlite.db')
        self.cursor = conn.cursor()

class StudentDao:
    # C
    def create(self):

        cursor = self.cursor

        try:
            cursor.execute("drop table students")
        except sqlite3.OperationalError as err :
            print("테이블이 존재하지 않습니다.")

        cursor.execute(
            '''create table students
            (id text primary key, pwd text, name text, birth text)'''
        )

        # query = "CREATE TABLE IF NOT EXISTS member"
        # query += "(userid VARCHAR(10) PRIMARY KEY, password VARCHAR(10), "
        # query += "phone VARCHAR(10), regdate DATE DEFAULT CURRENT_TIMESTAMP)"
        # self.conn.execute(query)
        cursor.commit()

    # C
    def insert_one(self, payload):
        # payload = ('kim', '김뫄뫄', '1989/11/11')
        cursor = self.cursor
        sql = f"insert into students(id, ped, name, birth) values('{payload.id}', '{payload.pwd}', '{payload.name}', '{payload.birth}')"
        cursor.execute(sql)
    
    # C
    def insert_many(self):
        data = [
            ('lee', '이솨솨', '1985/12/31'), ('park', '박롸롸', '1970/07/17'), ('choi', '최와와', '1950/06/06')
        ]
        query = "INSERT INTO mamber(id, pwd, name, birth) VALUES (?, ?, ?, ?)"
        self.cursor.executemany(query, data)
        self.cursor.commit()

    # R
    def fetch_by_id(self, id):
        cursor = self.cursor
        findID = 'park'
        sql = f"select * from students where id = '%?'"

        cursor.execute(sql, (id))

        result = cursor.fetchone()
        print(type(result)) # 튜플 형태로 리턴
        if result != None :
            print('아이디 : '+ result[0], end='')
            print(', 이름 : '+ result[1], end='')
            print(', 생일 : '+ result[2], end='')
        else:
            print('문제가 있습니다.')
        print('-'*20)

    def fetch_list(self):
        cursor = self.cursor
        sql = 'select * from students order by name desc'
        for id, name, birth in cursor.execute(sql):
            print(id + '#' + name + '#' + birth)
        print('-'*20)
        
    def fetch_by_name(self, name):
        cursor = self.cursor
        sql = f"select * from students where name like '%?%'"
        cursor.execute(sql, (name))
        return cursor.fetchall()

    def fetch_count(self):
        cursor = self.cursor
        query = 'select * from students'
        cursor.execute(query)
        rows = cursor.fetchall()
        count = 0
        for i in rows:
            count += 1
        return count

    # R
    def fetch_all(self):
        cursor = self.cursor
        cursor.execute('select * from students')
        return cursor.fetchall()
    
    # R
    def login(self, id, pwd):
        cursor = self.cursor
        sql = """
            select * from students where id like ? and pwd like ?
        """
        data = [id, pwd]
        cursor.execute(sql, data)
        return cursor.fetchone()

    # U
    def update(self, id, name):
        cursor = self.cursor
        sql = f"update students set name = ? where id = ?"
        cursor.execute(sql, (id, name))
        print(cursor.rowcount) # 성공 여부
        self.conn.commit()
    
    # D
    def delete(self):
        cursor = self.cursor
        sql = f"delete from students where id = ?"
        cursor.execute(sql, (id))
        print(cursor.rowcount)
        self.conn.commit()
        # cursor.close()
        # conn.close() web 상에서는 close 하지 않음

class StudentService:
    dao = StudentDao()
    def add_students(self, student):
        print('#### add_student ####')
        dao.insert_many()
