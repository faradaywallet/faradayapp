import pymysql.cursors

def connect_DB(c_host, c_port, c_user, c_password, c_db, enc_cc_num):
    try:
        connection = pymysql.connect(host = c_host, port= c_port, user = c_user, password = c_password, db= c_db, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        print('Connected to database')

        insert_statement = (
            "INSERT INTO creditcard (creditcardnum)"
            "VALUE (%s)"
        )

        data = str(enc_cc_num)
        with connection.cursor() as cursor:
            try:
                cursor.execute(insert_statement, data)
                connection.commit()
                print('Insert successful')
            except:
                print('Unable to insert into database')
    finally:
        connection.close()
