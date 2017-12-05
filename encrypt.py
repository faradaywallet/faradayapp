from nacl import secret, pwhash, utils
import os

class Encrypt():
    # Generates a new salt
    def generate_salt(self):
        salt = utils.random(pwhash.SCRYPT_SALTBYTES)
        return salt

    # Generate new symmetric key and returns a box with it as the payload
    def generate_key(self, password, salt):
        # generate key that will be used to encrypt inner box
        userKey = utils.random(secret.SecretBox.KEY_SIZE)

        # generate key that will be used to encrypt outer box
        key = pwhash.kdf_scryptsalsa208sha256(secret.SecretBox.KEY_SIZE, password, salt,
                                          opslimit=pwhash.SCRYPT_OPSLIMIT_INTERACTIVE,
                                          memlimit=pwhash.SCRYPT_MEMLIMIT_INTERACTIVE)
        nonce = utils.random(secret.SecretBox.NONCE_SIZE)

        box = secret.SecretBox(key)
        encrypted = box.encrypt(userKey, nonce)
        return encrypted

    # Generate a session key for a Flask session - must be used in conjunction with user's symmetric key for authorization process
    def generate_session_key(self):
        return os.urandom(24)

    # TODO: BEING WORKED ON. PLS IGNORE. BUT IT MIGHT WORK.
    def changed_password(self, box, oldPass, newPass, salt):
        outerKey = pwhash.kdf_scryptsalsa208sha256(secret.SecretBox.KEY_SIZE, oldPass, salt,
                                          opslimit=pwhash.SCRYPT_OPSLIMIT_INTERACTIVE,
                                          memlimit=pwhash.SCRYPT_MEMLIMIT_INTERACTIVE)

        outerBox = secret.SecretBox(outerKey)
        innerKey = outerBox.decrypt(box)

        nonce = utils.random(secret.SecretBox.NONCE_SIZE)

        newKey = pwhash.kdf_scryptsalsa208sha256(secret.SecretBox.KEY_SIZE, newPass, salt,
                                              opslimit=pwhash.SCRYPT_OPSLIMIT_INTERACTIVE,
                                              memlimit=pwhash.SCRYPT_MEMLIMIT_INTERACTIVE)

        newOuterBox = secret.SecretBox(newKey)
        encryptedOuterBox = newOuterBox.encrypt(innerKey, nonce)

        return encryptedOuterBox

    # Decrypts the box containing the symmetric key using a user's password and salt
    def decrypt_key(self, box, password, salt):
        # noinspection PyBroadException
        try:
            key = pwhash.kdf_scryptsalsa208sha256(secret.SecretBox.KEY_SIZE, password, salt,
                                              opslimit=pwhash.SCRYPT_OPSLIMIT_INTERACTIVE,
                                              memlimit=pwhash.SCRYPT_MEMLIMIT_INTERACTIVE)

            outerBox = secret.SecretBox(key)
            symKey = outerBox.decrypt(box)
            return symKey

        except:
            return -1

    # Encrypts a payload with the user's symmetric key. Returns the encrypted payload.
    def encrypt_payload(self, symKey, payload):
        payload = payload.encode()
        nonce = utils.random(secret.SecretBox.NONCE_SIZE)

        box = secret.SecretBox(symKey)
        encrypted = box.encrypt(payload, nonce)

        return encrypted

    # Decrypts the payload using the user's symmetric key. Returns the payload if successful, and -1 if not
    def decrypt_payload(self, symKey, payload):
        # noinspection PyBroadException
        try:
            box = secret.SecretBox(symKey)
            contents = box.decrypt(payload)
            return contents.decode()
        except:
            return -1






# dynamicAdd = [string of stuff to add]
# cards = soup.find(id="cardList")
# cards.append(dynamicAdd)