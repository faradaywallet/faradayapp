from db_controller import FaradayDB
from encrypt import Encrypt

Encrypt = Encrypt()
db = FaradayDB('localhost', 3310, 'root', 'cybr200', 'faraday')

def test_insert_user(values):
    insert_statement = (
        "INSERT INTO test_table (name, email)"
        "VALUE (%s, %s)"
    )
    db.insert_row(insert_statement, values)

def test_insert_full_user():
    '''
    Test registration logic, including encrypted storage
    :param values=(user, email, createDate, salt, auth, symmetricBox):
    '''

    user = 'testuser'
    email = 'test@email.com'
    createDate = '12042017'
    password = b'testpwd'

    salt = Encrypt.generate_salt()
    session_key = Encrypt.generate_session_key()
    sym_key_box = Encrypt.generate_key(password, salt)

    values=(user, email, createDate, str(salt), str(session_key), str(sym_key_box))

    insert_statement = (
        "INSERT INTO user (user, email, createDate, salt, auth, symmetricBox)"
        "VALUE (%s, %s, %s, %s, %s, %s)"
    )
    db.insert_row(insert_statement, values)\

def test_select_specific_user():
    select_statement = ('SELECT * FROM user WHERE user=%s')
    db.start()
    rows = db.connection.cursor()
    rows.execute(select_statement, 'testuser')
    print('DBCONTROL/SUCCESS: Select query successful:', select_statement, 'testuser')
    for data in rows:
        print(data)
    rows.close()
    db.close()

def test_insert_credit(values):
    insert_statement = (
        "INSERT INTO test_credit (credit, notes)"
        "VALUE (%s, %s)"
    )
    db.insert_row(insert_statement, values)


def test_select_credit():
    print('DBCONTROL/LOG: Starting db connection')
    select_statement = (
        "SELECT * FROM test_credit"
    )
    db.start()
    rows = db.connection.cursor()
    rows.execute(select_statement)
    print('DBCONTROL/SUCCESS: Select query successful:', select_statement)
    for data in rows:
        print(data)
    rows.close()
    db.close()

if __name__ == '__main__':
    test_select_credit()
    test_select_specific_user()

