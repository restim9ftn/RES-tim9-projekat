import socket
import pickle
import subprocess
import time
from hashlib import sha256
from random import randint
from time import sleep
from datetime import date,datetime

from LocalDevice import LocalDevice

class NevalidanUnos(Exception):
    def __init__(self, message=None):
        self.message = message
        
    def __str__(self):
        if self.message is None:
            return "Nevalidan unos."
        return self.message

def Menu(nizuredjaja,tipuredjaja):
   
    print("1. Upali uredjaj")
    print("2. Ugasi uredjaj")
    print("3. Ugasi program")
    try:

        option1 = int(input("Unesi komandu: "))
        if (option1< 0  or option1 > 3):
            raise NevalidanUnos("pogresan unos")
    except NevalidanUnos as e:
        print(e)
        return None
    except Exception:
        print("Unesite komandu")
        return None
            
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
        mode=input("Unesite 'ams' ako zelite da direktno saljete ams procesu, ili 'controller' ako zelite kontroleru: ")
        localDevice = LocalDevice(tip,val,timestamp,hash)
        nizuredjaja.append(localDevice)
        if mode!='ams':
            subprocess.call(f'start python LokalniUredjaj/main.py{tip} {val} {timestamp} {hash} {mode}',shell = True)
            subprocess.call(f'start python LokalniKontroler/main.py', shell=True)
           
        subprocess.call(f'start python LokalniUredjaj/main.py {tip} {val} {timestamp} {hash} {mode}', shell=True)
        
        
    elif(option1==2):
        print("Koji uredjaj zelite da ugasite?")
        for i in range(0,len(nizuredjaja)):
            print(str(i)+". "+str(tipuredjaja[i]))
            option2 = int(input("Unesi komandu: "))
            val=nizuredjaja[option2].getValue()
            tdy=nizuredjaja[option2].getDeviceType()
            timestamp=nizuredjaja[option2].getTimeStamp()
            hash=nizuredjaja[option2].getHash()
            mode=input("Unesite ugasi ako zelite da ugasite uredjaj: ")

        #if mode == 'ugasi':
            try:
                TCP_IP = '127.0.0.1'
                TCP_PORT = 5555
                MESSAGE = pickle.dumps(mode)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                s.send(MESSAGE)
                s.close()
            except Exception:
                print("Exception")
        #for i in range(0,len(nizuredjaja)):
        #   print(str(i)+". "+nizuredjaja[i].toString())
        #option2 = int(input("Unesi komandu: "))
        
    elif(option1==3):
        print("Gasenje")
        quit()

    else:
        print("Pogresna komanda!")
    return True

if __name__=="__main__":
    tipuredjaja =["digital","analog"]
    nizuredjaja=[]
    subprocess.call(f'start python AMS/main.py', shell=True)
    while(Menu(nizuredjaja,tipuredjaja)):
        print("Working...")