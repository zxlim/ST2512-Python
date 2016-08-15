#!/usr/bin/python
import socket
import threading
import Queue

def listener(c, addr, q):
    with lock:
        clients.add(c)
    c.settimeout(3.0)
    while True:
        try:
            buffer = c.recv(255)
            if len(buffer) > 0:
                print(buffer)
            else:
                q.put("q")
                break
            with lock:
                for i in clients:
                    i.sendall(buffer)
        except Exception as ex:
            if not check or (str(ex) != "timed out"):
                q.put("q")
                break;
    with lock:
        clients.remove(c)
    c.close()
    print("Connection from " + addr + " closed.")
    return

def getSocket():
    return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "0.0.0.0"
port = 8089
clientcount = 0
s = getSocket()
s.bind((host, port))
s.listen(5)
s.settimeout(3.0)
check = True
q = Queue.Queue(10)
clients = set()
lock = threading.Lock()
    
print("Server connection started.\nListening on " + host + ":"\
      + str(port) + " for incoming connections")

while True:
    if check:
        try:
            c, addr = s.accept()
            clientcount = clientcount + 1
            print("Remote connection from " + addr[0] + " accepted.")
            print("Clients connected: " + str(clientcount))
            thread = threading.Thread(target=listener, args=(c, addr[0], q))
            thread.start()
        except Exception as ex:
            if str(ex) != "timed out":
                break
    else:
        if clientcount == 0:
            break
    if not q.empty():
        clientcount = clientcount - 1
        print("Clients connected: " + str(clientcount))
        if clientcount <= 0:
            check = False
if not check and clientcount <= 0:
    s.close()
    print("Server connection closed.")
