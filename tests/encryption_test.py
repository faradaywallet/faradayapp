from encrypt import Encrypt
import base64

Encrypt = Encrypt()

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
    full_encryption_test()
