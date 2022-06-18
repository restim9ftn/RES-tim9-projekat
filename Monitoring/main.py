import socket
import pickle
import subprocess
import time
from hashlib import sha256
from random import randint
from time import sleep
from datetime import date,datetime

def Menu(nizuredjaja,tipuredjaja):
   
    print("1. Upali uredjaj")
    print("2. Ugasi uredjaj")
    print("3. Ugasi program")
    option1 = int(input("Unesi komandu: "))
    option2=0
    option3=0
    if(option1==1):
        print("Koji uredjaj zelite da upalite?")
        for i in range(0,len(tipuredjaja)):
            print(str(i)+". "+str(tipuredjaja[i]))
        option2 = int(input("Unesi komandu: "))
        if(option2==0):
            tip='0'
        elif(option2==1):
            tip='1'
        val=int(input('Unesite vrednost:'))
        tdy=date.today().strftime("%d/%m/%Y")
        timestamp=datetime.timestamp(datetime.strptime(tdy,"%d/%m/%Y"))
        hash=sha256((input("Unesite naziv: ").encode())).hexdigest()
        mode=input("Unesite 'ams' ako zelite da direktno saljete ams procesu, ili controller ako zelite kontroleru. ")
        if mode!='ams':
            subprocess.call(f'start python LokalniKontroler/main.py', shell=True)
        subprocess.call(f'start python LokalniUredjaj/main.py {tip} {val} {timestamp} {hash} {mode}', shell=True)
    
    elif(option1==2):
        for i in range(0,nizuredjaja.count):
            print(i+". "+nizuredjaja[i].toString())
        option2 = int(input("Unesi komandu: "))
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5555
        MESSAGE = pickle.dumps('ugasi')
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        s.close()
        
    elif(option1==3):
        for i in range(0,nizuredjaja.count):
            print("Gasenje")
            return False
    else:
        print("Pogresna komanda!")
    return True

if __name__=="__main__":
    tipuredjaja =["digital","analog"]
    nizuredjaja=[]
    subprocess.call(f'start python AMS/main.py', shell=True)
    while(Menu(nizuredjaja,tipuredjaja)):
        print("Working...")