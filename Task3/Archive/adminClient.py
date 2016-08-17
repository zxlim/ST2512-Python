#!/usr/bin/python
from Crypto.Cipher import AES
from Crypto import Random
from hashlib import sha512
from socket import socket
import base64

def generateIV():
    return Random.new().read(16)

def encrypt(message, iv):
    key = sha512("KpbMNsKy8Pg9mTWEFq7oegbdcrhA").hexdigest()[:32]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return cipher.encrypt(message.encode("UTF-8"))

def decrypt(data):
    line = data.replace("\n", "").split("$")
    iv = base64.b64decode(line[1])
    message = line[2]
    key = sha512("KpbMNsKy8Pg9mTWEFq7oegbdcrhA").hexdigest()[:32]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    return (cipher.decrypt(message)).decode("UTF-8")

s = socket()
host = "192.168.1.11"
port = 35565
s.connect((host, port))
flag = True

print("Connected to server " + host + ":" + str(port))
user = raw_input("Enter your name:\t")

while flag:
    iv = generateIV()
    msg = raw_input("Chat:\t")
    data = user + "$" + base64.b64encode(iv) + "$" + encrypt(msg, iv)
    s.send(data)
    if (msg != "q") or (msg != "x"):
        recData = s.recv(2048)
        line = data.replace("\n", "").split("$")
        buffer = decrypt(recData)
        print(line[0] + ":\t" + buffer)
    if msg == "q" or msg == "x":
        flag = False
        break
s.close()
print("Connection to server closed.")
