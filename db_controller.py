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
            "INSERT INTO card (userid, cardid, createDate, salt, auth, symmetricBox)"
            "VALUE (%s, %s, %s, %s, %s, %s)"
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

    # def select_user(self):


    def close(self):
        print('DBCONTROL/LOG: Closing db connection')
        self.connection.close()

if __name__ == '__main__':
    db = FaradayDB('localhost', 3310, 'root', 'cybr200', 'faraday')
    db.test_select_credit()