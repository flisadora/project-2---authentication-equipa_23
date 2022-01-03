from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import cryptography.exceptions
import base64
import os
import hashlib
from Crypto.Cipher import DES

def pad(text):
    n = 8 - (len(text) % 8)
    return text + (b' ' * n)

def decryptDES(nonce, password, values):
    key = password + nonce
    # print(key)
    m = hashlib.md5(key)
    key = m.digest()

    des = DES.new(key[:8], DES.MODE_ECB)
    res = {}
    for v in values:
        res[v] = des.decrypt(toBinary(values[v])).decode().strip()
    return res

def encryptDES(password, values):
    nonce = os.urandom(8)
    key = password + nonce
    # print(key)
    m = hashlib.md5(key)
    key = m.digest()

    des = DES.new(key[:8], DES.MODE_ECB)
                
    res = {"salt": toString(nonce)}
    for v in values:
        res[v] = toString(des.encrypt(pad(values[v].encode())))
    return res

def toBinary(value):
    return base64.b64decode(value.encode('utf-8'))

def toString(value):
    return base64.b64encode(value).decode()

def doPBKDF2(salt, value, verify_value):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt = salt,
        iterations=500000,
        backend=default_backend()
    )

    try:
        kdf.verify(value, verify_value)
        return True
    except cryptography.exceptions.InvalidKey:
        return False