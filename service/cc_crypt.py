import os
from Cryptodome.Cipher import AES
from Cryptodome.Util import Counter

def encrypt(key, plaintext):
    ctr = Counter.new(128)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return aes.encrypt(plaintext.encode())

def decrypt(key, ciphertext):
    ctr = Counter.new(128)
    aes = AES.new(key, AES.MODE_CTR, counter=ctr)
    return aes.decrypt(ciphertext)

def generate_key():
    key = os.urandom(32)
    return key
