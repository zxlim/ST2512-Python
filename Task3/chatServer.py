#!/usr/bin/python
import socket
import threading
import Queue
import time

def listener(c, addr, q):
    name = ""
    chat = True
    with lock:
        clients.append(c)
    c.settimeout(3.0)
    print("Clients connected: " + str(len(clients)))
    try:
        buffer = c.recv(255)
        name = getUser(buffer)
        if name in users:
            c.sendall("Username already taken! Please try another.")
            q.put("q")
            chat = False
            time.sleep(3)
        else:
            print(name + " joined the chat.")
            with lock:
                users.append(name)
    except Exception as ex:
        if not check or (str(ex) != "timed out"):
            q.put("q")
            chat = False
    while chat:
        try:
            buffer = c.recv(255)
            if len(buffer) > 0:
                print(buffer)
            else:
                q.put("q")
                break
            with lock:
                for con in clients:
                    con.sendall(buffer)
        except Exception as ex:
            if not check or (str(ex) != "timed out"):
                q.put("q")
                break;
    c.close()
    with lock:
        clients.remove(c)
        for con in clients:
            con.sendall(name + " disconnected from the chat.\n")
            con.sendall(str(len(clients)) + " person(s) left in the chat.\n")
    print("Connection from " + addr + " closed.")
    print("Clients connected: " + str(len(clients)))
    return

def getUser(buf):
    buf = buf.split("]")[0]
    name = buf.replace("[", "")
    return name

def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0.0.0.0"
port = 8089
s = getSocket()
s.bind((host, port))
s.listen(10)
s.settimeout(3.0)
check = True
q = Queue.Queue(10)
clients = []
users = []
lock = threading.Lock()
    
print("Server connection started.\nListening on " + host + ":"\
      + str(port) + " for incoming connections")

while True:
    if check:
        try:
            c, addr = s.accept()
            print("Remote connection from " + addr[0] + " accepted.")
            thread = threading.Thread(target=listener, args=(c, addr[0], q))
            thread.start()
        except Exception as ex:
            if str(ex) != "timed out":
                break
    else:
        if len(clients) == 0:
            break
        else:
            check = True
    if not q.empty():
        if len(clients) == 0:
            check = False
            #print(str(check)) #Debug code
s.close()
print("Server connection closed.")
