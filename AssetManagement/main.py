from dataclasses import dataclass
from queue import Empty
import socket
import mysql.connector
import os
from _thread import *
from mysql.connector import Error


ASMSocket = socket.socket()
host = '127.0.0.1'
port = 2000
FORMAT = 'utf-8'

try:
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         database= 'projekat',
                                         password='andrija')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("KOnektovali ste se na MySQL Server verzija: ", db_Info)
        cursor = connection.cursor()
        cursor.execute("USE projekat;")
        cursor.execute("INSERT INTO devices(id,value) VALUES(7,'andrija');")
        connection.commit()
        record = cursor.fetchone()
        print("Uspesno ste se konektovali na bazu: ", record)

except Error as err:
    print("Greska prilikom konektovanja na bazu: ", err)



ThreadCounter = 0 
try:
    ASMSocket.bind((host, port)) 
except socket.error as err:
    print(err)

print("Server osluskuje i ceka poruke od klijenata....")
ASMSocket.listen(5)
def multi_client(connection):
    connection.send(str.encode("Server radi"))
    while True:
        data = connection.recv(2048)
        response = "Poruka: " + data.decode(FORMAT)
        if  data==Empty:
            break
        print(response)
        connection.sendall(str.encode(response))
    connection.close()
while True:
    Client, address = ASMSocket.accept()
    print("Konektovan:\n")
    print(str(address[0]))
    print(str(address[1]))
    start_new_thread(multi_client, (Client, ))
    ThreadCounter += 1
    print("Redni broj Thread-a: " + str(ThreadCounter))

def Menu(nizuredjaja,tipuredjaja):
    print("1. Upali uredjaj")
    print("2. Ugasi uredjaj")
    print("3. Ugasi program")
    option1 = int(input("Unesi komandu: "))
    option2=0
    option3=0
    if(option1==1):
        print("Koji uredjaj zelite da upalite?")
        for i in range(0,tipuredjaja.count):
            print(i+". "+tipuredjaja[i])
        option2 = int(input("Unesi komandu: "))
    elif(option1==2):
        for i in range(0,nizuredjaja.count):
            print(i+". "+nizuredjaja[i].toString())
        option2 = int(input("Unesi komandu: "))
    elif(option1==3):
        for i in range(0,nizuredjaja.count):
            print("Gasenje")
    else:
        print("Pogresna komanda!")

if connection.is_connected():
    cursor.close()
    connection.close()
    print("Konekcija sa bazom je prekinuta")

ASMSocket.close()