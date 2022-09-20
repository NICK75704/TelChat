from fileinput import close
import socket, threading
from time import time, sleep
import datetime
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ""
PORT = 51234
userSet = False
listen = False
wl = open("log.txt" , "a")
rl = open("log.txt" , "r")
content = rl.readlines()
clients = []
welcome = "Hello!\nTo exit, type 'control' + ']'\nto send a message, type your message followed by the enter key\nClients connected: "
newClientStr = "\na new client has connected\n"

def init():
  s.bind((HOST, PORT))
  s.listen()   
  while True:   
    conn, addr = s.accept() 
    threadClient = threading.Thread(target=connection, args=(conn, addr, clients, newClientStr, welcome))
    threadClient.start()

def sending(clients, conn, outgoingMessage):
  for client in clients:
    if client != conn:
      with open("log.txt") as rl:
        reply = str(str("\n" + outgoingMessage + "\n"))
        client.sendall(bytes(reply, "ascii"))
        print("message sent!")

def newClient(newClientStr, clients, welcome, conn):
    currentClient = clients[-1]
    clientCount = str(len(clients)) + " clients connected\n"
    for client in clients:
      if client != conn:
        client.sendall(bytes(newClientStr, "ascii"))
    currentClient.sendall(bytes(str(welcome + clientCount + "Please enter your nickname; if left empty, will default to IP Address\n"), "ascii"))
    print("client welcome'd")

def connection(conn, addr, clients, newClientStr, welcome):
  with open("log.txt") as rl:
    nickname = str(f"{addr}")
    messages = sum(1 for line in rl)
    clients.append(conn)
    print("registered client")
    print("current clients " + str(clients))
    print(f"Incoming connection from {addr}")
    newClient(newClientStr, clients, welcome, addr)
    while True:
      input = str(conn.recv(1024), "ascii")
      timestamp = datetime.datetime.now()
      if input:
        try:
          incomingMessage = str(timestamp.strftime("%c") + ", " + nickname + ": " + input)
          with open("log.txt" , "a") as wl:
            print(incomingMessage)
            wl.write(incomingMessage)
            wl.write("\n")
          messages = messages + 2
          sending(clients, conn, incomingMessage)
        except:
          clients.remove(conn)
          conn.close
          break
  
init()