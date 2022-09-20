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
newClientStr = f"\na new client has connected, there are "

def disconnect(conn, clients, clientCount):
  for client in clients:
    if client != conn:
      with open("log.txt") as rl:
        reply = str(str("client disconnected " + clientCount + " clients connected"))
        client.sendall(bytes(reply, "ascii"))
        print("message sent!")
  clients.remove(conn)
  conn.close

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
        client.sendall(bytes(newClientStr + clientCount, "ascii"))
    currentClient.sendall(bytes(str(welcome + clientCount + "\n"), "ascii"))
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
      clientCount = str(len(clients))
      input = conn.recv(1024)
      message = str(input, "ascii")
      timestamp = datetime.datetime.now()
      print("*" + str(bytes(input)) + "*")
      try:
        if input == bytes(b''):
          disconnect(conn, clients, clientCount)
          break
        if input != bytes(b'\r\n') and input != bytes(b'\x1b[A\r\n') and input != bytes(b'\x1b[B\r\n') and input != bytes(b'\x1b[C\r\n') and input != bytes(b'\x1b[D\r\n'):
          print(message)
          if input == bytes(b'exit\r\n'):
            print("bruh")
            disconnect(conn, clients, clientCount)
            break
          if message.startswith("/nickname"):
            nickname = message[10:].replace("\r\n", "")
          else:
            incomingMessage = str(timestamp.strftime("%c") + ", " + nickname + ": " + message)
            with open("log.txt" , "a") as wl:
              print(incomingMessage)
              wl.write(incomingMessage)
              wl.write("\n")
            messages = messages + 2
            sending(clients, conn, incomingMessage)
        elif input == bytes(b'\r\n'):
          pass
      except:
        disconnect(conn)
        break
  
init()