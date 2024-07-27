import hashlib
import datetime
import base64
import os
import encryptme
import time
import random

def try_init():
    try:
        os.mkdir("idx")
        os.mkdir("raw")
    except FileExistsError:
        pass

def create_site(name: str):
    raw = hashlib.md5(str(os.urandom(256).hex()).encode()).hexdigest()
    idx = hashlib.sha512(name.encode()).hexdigest()
    os.mkdir("raw/" + raw)
    os.mkdir("raw/" + raw + "/idx")
    os.mkdir("idx/" + idx)
    with open("idx/" + idx + "/indexfile", "w") as file:
        file.write(encryptme.encrypt(name, raw).decode())
    return [raw, idx, name]

def lookup(name: str):
    idx = hashlib.sha512(name.encode()).hexdigest()
    with open("idx/" + idx + "/indexfile", "r") as index:
        id = encryptme.decrypt(name, index.read())
    return id

def generate_s3(name: str, path: str):
    id = lookup(name).decode()
    s1 = hashlib.sha512(name.encode()).hexdigest()
    s2 = hashlib.sha512(path.encode()).hexdigest()
    s3 = hashlib.sha512((s1 + s2 + id).encode()).hexdigest()
    return s3

def create_path(name: str, path: str):
    id = lookup(name).decode()
    s3 = generate_s3(name, path)
    if os.path.exists("raw/" + id + "/idx/" + s3):
        raise FileExistsError
    with open("raw/" + id + "/idx/" + s3, "w") as index:
        index.write(encryptme.encrypt(s3 + path + name, hashlib.md5(str(os.urandom(256).hex()).encode()).hexdigest()).decode())

def create_document(name: str, path: str, document: str, data: str):
    id = lookup(name).decode()
    s3 = generate_s3(name, path)
    with open("raw/" + id + "/idx/" + s3, "r") as index:
        idx = index.read()
    s4 = generate_s3(name, document+idx)
    with open("raw/" + id + "/" + s4, "w") as doc:
        doc.write(encryptme.encrypt(s4 + path + name + document, data).decode())

def read_document(name: str, path: str, document: str):
    id = lookup(name).decode()
    s3 = generate_s3(name, path)
    with open("raw/" + id + "/idx/" + s3, "r") as index:
        idx = index.read()
    s4 = generate_s3(name, document+idx)
    with open("raw/" + id + "/" + s4, "r") as doc:
        c = doc.read()
    return encryptme.decrypt(s4 + path + name + document, c)