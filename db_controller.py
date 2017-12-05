__author__ = 'Bren'

import pymysql.cursors

class FaradayDB:
    def __init__(self, c_host, c_port, c_user, c_password, c_db):
        self.connection = ''
        self.c_host = c_host
        self.c_port = c_port
        self.c_user = c_user
        self.c_password = c_password
        self.c_db = c_db

    def start(self):
        try:
            self.connection = pymysql.connect(host=self.c_host,
                                              port=self.c_port,
                                              user=self.c_user,
                                              password=self.c_password,
                                              db=self.c_db,
                                              charset='utf8', cursorclass=pymysql.cursors.DictCursor)
            print('DBCONTROL/SUCCESS: Connection successful to', self.c_db)
        except:
            print('DBCONTROL/FAIL: Unable to connect to database', self.c_db)

    def insert_user(self, values):
        insert_statement = (
            "INSERT INTO user (user, email, createDate, salt, auth, symmetricBox)"
            "VALUE (%s, %s, %s, %s, %s, %s)"
        )
        self.insert_row(insert_statement, values)

    def insert_credit(self, values):
        insert_statement = (
            "INSERT INTO card (userid, payload)"
            "VALUE (%s, %s)"
        )
        self.insert_row(insert_statement, values)

    def insert_row(self, insert_statement, values):
        print('DBCONTROL/LOG: Starting db connection')
        self.start()
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(insert_statement, values)
                self.connection.commit()
                print('DBCONTROL/SUCCESS: Insert successful:', values)
            except:
                print('DBCONTROL/FAIL: Unable to insert into database:', values)
        self.close()

    def select_data(self, select_statement, value):
        self.start()
        data = self.connection.cursor()
        try:
            data.execute(select_statement, value)
            print('DBCONTROL/SUCCESS: Select query successful:', select_statement, value)
        except:
            print('DBCONTROL/FAIL: Select query failed:', select_statement)
        data.close()
        self.close()
        return data

    # TODO: Consider refactoring the following:
    def get_session_key(self, user):
        select_statement = ('SELECT auth FROM user WHERE user=%s')
        data = self.select_data(select_statement, user)
        session_key = data.fetchone()["auth"]
        return session_key

    def get_symmetric_box(self, user):
        select_statement = ('SELECT symmetricBox FROM user where user=%s')
        data = self.select_data(select_statement, user)
        symmetric_box = data.fetchone()["symmetricBox"]
        return symmetric_box

    def get_salt(self, user):
        select_statement = ('SELECT salt FROM user where user=%s')
        data = self.select_data(select_statement, user)
        salt = data.fetchone()["salt"]
        return salt

    def get_email(self, user):
        select_statement = ('SELECT email FROM user where user=%s')
        data = self.select_data(select_statement, user)
        email = data.fetchone()["email"]
        return email

    def get_payloads(self, user):
        select_statement = ('SELECT payload FROM card where userid=%s')
        data = self.select_data(select_statement, user)
        payloads = data.fetchall()
        return payloads

    def close(self):
        print('DBCONTROL/LOG: Closing db connection')
        self.connection.close()