import socket
import os

Client1 = socket.socket() 
host = '127.0.0.1'
port = 2000

Client2 = socket.socket()  
host1 = '127.0.0.1'
port1 = 2001



try:
    Client1.connect((host, port))
    Client2.connect((host1, port1))
    print("Cekamo na odgovor od servera.....")
    odgovor = Client1.recv(1024)
    odgovor = Client2.recv(1024)
except socket.error as err:
    print("Problem pri konektovanju", err)




while True:
    print("Izaberite na koga zelite da se konektujete: \n")
    print("1-ASM\n")
    print("2-LK\n")   
    x = int(input("Izbor:\n"))
    if x==1 :
        y = input("Unesite poruku ASM-u: ")
        Client1.send(str.encode(y))
    elif x==2:
        y= input("Unesite poruku LK-u: ")
        Client2.send(str.encode(y))
    elif x==0:
        print("Izlazim...")
        break
    else:
        print("Nije uneta validna vrednost ")
        

Client1.close()
Client2.close()