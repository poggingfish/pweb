from cryptography.fernet import Fernet
import base64
import hashlib

def encrypt(password, text):
    cipher_suite = Fernet(base64.encodebytes(hashlib.sha256(password.encode()).digest()))
    return cipher_suite.encrypt(text.encode())

def decrypt(password, text):
    cipher_suite = Fernet(base64.encodebytes(hashlib.sha256(password.encode()).digest()))
    return cipher_suite.decrypt(text.encode())