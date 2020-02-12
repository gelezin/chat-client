#the classic imports
import socket
import threading
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostAddress = ("18.195.107.195", 5378)
sock.connect(hostAddress)

username = input("Please enter a non-existing single word username:\n")
splitUsername = username.split(" ")
if len(splitUsername) != 1:
    print(f"{username} is not one word\n")
    username = input("Please enter another username:\n")

def initalHandshake():
    stringBytes = f"HELLO-FROM {username}\n".encode("utf-8")
    sock.sendall(stringBytes)
    recieve()

def userSend(message):
    if message.startswith("SEND"):
        sent = message.split(sep=" ", maxsplit=3)[2]
        print(username + " : " + sent)
    message += "\n"
    stringBytes = message.encode("utf-8")
    sock.sendall(stringBytes)

def recieve():
    msg = sock.recv(2048).decode(encoding='UTF-8')
    if msg == '':
        raise RuntimeError("Socket connection broken")
    if msg.startswith("IN-USE"):
        sock.close()
        print("Username was taken. Try again")
        sys.exit(0)
    elif msg.startswith("HELLO"):
        message = msg.split(sep=" ", maxsplit=2)[1]
        print(f"SERVER : Hello {message}")
    elif msg.startswith("WHO-OK"):
        message = msg.split(maxsplit=2, sep=" ")[1]
        print(f"SERVER : Users ; {message}")
    elif msg.startswith("DELIVERY"):
        sender = msg.split(maxsplit=3, sep=" ")[1]
        message = msg.split(maxsplit=3, sep=" ")[2]
        print(f"{sender} : {message}")
    else:
        print(msg)

try:
    initalHandshake()
    print("Chat functions:\n WHO; sends a list of all users\n SEND <user> <msg>; sends a message to that user\n !quit; closes the chat\n")
    while True:
        recieveT = threading.Thread(target=recieve)
        recieveT.start()
        message = input()
        if message != "!quit":
            sendT = threading.Thread(target=userSend, args=(message,))
            sendT.start()
            sendT.join()
        else:
            break

except OSError as msg:
    print(msg)

finally:
    sock.close()
    print("Connection closed\n")
    sys.exit(0)
