from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import cryptography.exceptions
# from cryptography.fernet import Fernet
import base64
import os
import json
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



# ----------------------------------------------------------------

# # password = input("Password: ")
# user = "user"
# user = user.encode()
# # salt = os.urandom(8)
# salt = "wK4dRIydjfJqWpcjXjqD0A==".encode()

# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt = salt,
#     iterations=500000,
#     backend=default_backend()
# )

# secret_user = kdf.derive(user)
# print("Secret_user:", base64.b64encode(secret_user))
# password = "userpassword"
# password = password.encode()

# # salt = os.urandom(8)
# # salt = b"\x02\xae\x0b\xdf\xe8\x84_\x85"

# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt = salt,
#     iterations=500000,
#     backend=default_backend()
# )

# secret = kdf.derive(password)
# # key = base64.urlsafe_b64encode(secret)
# # f = Fernet(key)
# print("Salt: ", salt)
# print("Secret: ", secret)

# # with open("passwords.json") as f:
# #     password = secret
# #     nonce1 = os.urandom(8)
# #     # nonce2 = os.urandom(8)
# #     key1 = password + nonce1
# #     print(key1)
# #     # key2 = password + nonce2
# #     m1 = hashlib.md5(key1)
# #     # m2 = hashlib.md5(key2)
# #     key1 = m1.digest()
# #     # key2 = m2.digest()

# #     def pad(text):
# #         n = 8 - (len(text) % 8)
# #         return text + (b' ' * n)

# #     dns = b"http://localhost:8000/server/login.php" # o q queremos encripter
# #     email1 = b"lili_martinha@gmail.com" # o q queremos encripter
# #     # email2 = b"john@gmail.com" # o q queremos encripter
# #     password1 = b"AvadaKedravaBellatrix88" # o q queremos encripter
# #     # password2 = b"AvadaKedravaBellatrix" # o q queremos encripter
# #     des1 = DES.new(key1[:8], DES.MODE_ECB)
# #     # des2 = DES.new(key2[:8], DES.MODE_ECB)

# #     padded_dns = pad(dns)
# #     # print(len(padded_dns))
# #     # print(len(dns), len(dns) % 8)
# #     padded_email1 = pad(email1)
# #     # padded_email2 = pad(email2)
# #     padded_password1 = pad(password1)
# #     # padded_password2 = pad(password2)
# #     encrypted_dns1 = des1.encrypt(padded_dns)
# #     # encrypted_dns2 = des2.encrypt(padded_dns)
# #     encrypted_email1 = des1.encrypt(padded_email1)
# #     # encrypted_email2 = des2.encrypt(padded_email2)
# #     encrypted_password1 = des1.encrypt(padded_password1)
# #     # encrypted_password2 = des2.encrypt(padded_password2)

# #     print(base64.b64encode(encrypted_dns1).decode('utf-8'))
# #     print(encrypted_dns1)
# #     print(des1.decrypt(encrypted_dns1))
# #     print(des1.decrypt(encrypted_email1))
# #     print(des1.decrypt(encrypted_password1))

# #     data = json.load(f)
# #     d = {"username": base64.b64encode(secret_user).decode('utf-8'), "password": base64.b64encode(secret).decode('utf-8'), "salt": base64.b64encode(salt).decode('utf-8'),
# #                 "logins": [
# #                     {"dns": base64.b64encode(encrypted_dns1).decode('utf-8'), "email": base64.b64encode(encrypted_email1).decode('utf-8'), "password": base64.b64encode(encrypted_password1).decode('utf-8'), "salt": base64.b64encode(nonce1).decode('utf-8')}
# #                     # {"dns": base64.b64encode(encrypted_dns2).decode('utf-8'), "email": base64.b64encode(encrypted_email2).decode('utf-8'), "password": base64.b64encode(encrypted_password2).decode('utf-8'), "salt": base64.b64encode(nonce2).decode('utf-8')}
# #                 ]}
    
# #     data["users"].append(d)
# # with open("passwords.json", "w") as f:
# #     json.dump(data, f)

# #     # , 
# #     #         {
# #     #             "username": "",
# #     #             "password": "",
# #     #             "salt": "",
# #     #             "logins": [
# #     #                 {"dns": "Harry Potter Wiki", "username": "lilimarta74", "email": "lili_martinha@gmail.com", "password": "AvadaKedravaBellatrix88"}
# #     #             ]
# #     #         }

# # token = f.encrypt(password)
# # print(token)


# kdf = PBKDF2HMAC(
#     algorithm=hashes.SHA256(),
#     length=32,
#     salt = salt,
#     iterations=500000,
#     backend=default_backend()
# )
# # print(f.decrypt(token))
# try:
#     kdf.verify(password, secret)
#     print("Password did match")
# except cryptography.exceptions.InvalidKey:
#     print("Password did not match")