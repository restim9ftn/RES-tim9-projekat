from audioop import add
from gettext import NullTranslations
from queue import Empty
import socket
import os
from _thread import *

FORMAT = 'utf-8'

ASMSocket = socket.socket() #AssetManagerSocket
host = '127.0.0.1'
port = 2000


LKSocket = socket.socket() #Lokalni kontroler socket
host1 = '127.0.0.1'
port1= 2001


try:
    LKSocket.bind((host1, port1))
    ASMSocket.connect((host, port))
    odgovor = ASMSocket.recv(1024)
    print("Server osluskuje....")
    LKSocket.listen(5)
except socket.error as err:
    print("Problem pri konektovanju..", err)

ThreadCounter = 0

def multi_client(connection):
    connection.send(str.encode("Kontroler radi.."))
    while True:
        data = connection.recv(2048)
        response = "Poruka: " + data.decode(FORMAT)
        if  data==Empty:
            break
        ASMSocket.send(data)
        response.replace('Poruka:', '')
        ASMSocket.send(str.encode(response)) 
        print(response) 
        response.replace('Poruka:', '')
        connection.sendall(str.encode(response))
    connection.close()
while True:
    Client, address = LKSocket.accept()
    print("Konektovan:\n")
    print(str(address[0]))
    print(str(address[1]))
    start_new_thread(multi_client, (Client, ))
    ThreadCounter += 1
    print("Redni broj Thread-a: " + str(ThreadCounter))

LKSocket.close()
ASMSocket.close()