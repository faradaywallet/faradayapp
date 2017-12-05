from encrypt import Encrypt
import json

Encrypt = Encrypt()

def payload_encryption_test():
    password = b'testpwd'
    payload = {'ccnum': '1111222233334444', 'expdate': '09/13/2018', 'cvc': '123', 'notes': 'adding user notes'}

    salt = Encrypt.generate_salt()
    print('ENCRYPT\TEST: salt: ', salt)

    sym_key_box = Encrypt.generate_key(password, salt)
    print('ENCRYPT\TEST: sym_key_box: ', sym_key_box)

    sym_key = Encrypt.decrypt_key(sym_key_box, password, salt)
    print('ENCRYPT\TEST: sym_key: ', sym_key)

    # Payload encryption (encrypt the payload)
    json_payload_string = json.dumps(payload)
    print('JSON PAYLOAD:', json_payload_string)

    encrypted_payload = Encrypt.encrypt_payload(sym_key, json_payload_string.encode())
    print('ENCRYPT\TEST: encrypted_payload: ', encrypted_payload)

    decrypted_payload = Encrypt.decrypt_payload(sym_key, encrypted_payload)
    print('ENCRYPT\TEST: decrypted_payload: ', decrypted_payload)

    payload_dict = json.loads(decrypted_payload)
    print(payload_dict)
    print(payload_dict["ccnum"])
    print(payload_dict["expdate"])
    print(payload_dict["cvc"])
    print(payload_dict["notes"])


def full_encryption_test():
    user = 'testuser'
    password = b'testpwd'
    ccnum = '1111222233334444'

    salt = Encrypt.generate_salt()
    print('ENCRYPT\TEST: salt: ', salt)

    sym_key_box = Encrypt.generate_key(password, salt)
    print('ENCRYPT\TEST: sym_key_box: ', sym_key_box)

    sym_key = Encrypt.decrypt_key(sym_key_box, password, salt)
    print('ENCRYPT\TEST: sym_key: ', sym_key)

    # Payload encryption (encrypt the payload)
    encrypted_payload = Encrypt.encrypt_payload(sym_key, ccnum)
    print('ENCRYPT\TEST: encrypted_payload: ', encrypted_payload)

    decrypted_payload = Encrypt.decrypt_payload(sym_key, encrypted_payload)
    print('ENCRYPT\TEST: decrypted_payload: ', decrypted_payload)

if __name__ == '__main__':
    payload_encryption_test()
