import mysql.connector
from multiprocessing import Queue
import pickle
import select
import socket
from threading import Thread
from dicttoxml import dicttoxml
import xmltodict
import time
from datetime import datetime
from LocalDevice import LocalDevice 

receivequeue=Queue()

connector=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="andrija")

#prihvatanje apdejta deviceova
def ListenForMainControlerNotifications():
    HOST=''
    PORT=5017
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    print ("Listening on port 5017 for new notifications.")
    read_list = [ss]
    while True:
        try:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is ss:
                    client_socket, address = ss.accept()
                    read_list.append(client_socket)
                else:
                    data = s.recv(8192)
                    
                    if data:
                        device=pickle.loads(data)
                        
                        try:
                            if connector.is_connected()==True:
                                for i in device:
                                    cursor = connector.cursor()
                                    query="insert into res1.states (hash,timestamp,type,value) values (%s,%s,%s,%s)"
                                    val=(i.getHash(),i.getTimeStamp(),str(i.getDeviceType()),i.getValue())
                                    cursor.execute(query,val)
                                    connector.commit()
                                    print("Dodat uredjaj")
                        except Exception as e:
                            print(e)
                        # try:
                        #     s.send('ok'.encode())
                        # except Exception as e:
                        #     print(e)
                        # print('sent ok')                       
                    else:
                        print('closed')
                        s.close()
                        read_list.remove(s)
        except:
            print(readable)


def SaveChangesToDb():
    while(1):
        entity = receivequeue.get()
        print(entity)


def RetrieveAll():
        #today = datetime.now()
        #date = f"{today.month}/{today.year}";
        if connector.is_connected():
            query="select distinct hash from res1.states" 
            cursor = connector.cursor()
            cursor.execute(query)
            print('Values:\n')
            for u in cursor:
                print(f"Hash:{u[0]}")


def RetrieveAllByTime():
    fromDate=input('od: ')
    toDate=input('do: ')
    hash=input('hash: ')
    #today = datetime.now()
    #date = f"{today.month}/{today.year}";
    string = "01/01/2020"
    # pom=ciso8601.parse_datetime(string)
    # print(time.mktime(pom.timetuple()))
    #print(datetime(fromDate.split('/')[2],fromDate.split('/')[1],fromDate.split('/')[0],0,0).timestamp())
    fromTS=datetime.timestamp(datetime.strptime(fromDate,"%d/%m/%Y"))
    toTS=datetime.timestamp(datetime.strptime(toDate,"%d/%m/%Y"))
    print(fromTS)
    print(toTS)
    if connector.is_connected():
        query=f"select * from res1.states where timestamp<={toTS} and timestamp>={fromTS} and hash='{hash}'" 
        cursor = connector.cursor()
        cursor.execute(query)
        print('Values:\n')
        for u in cursor:
            print(f"Hash:{u[0]}, Timestamp:{u[1]}, Type:{u[2]}, Value: {u[3]}")


def LoadRadniSati():
    with open('./radnisaticonfig.xml') as fd:
        doc = xmltodict.parse(fd.read())
    return doc['time']['value']


def BrojRadnihSati():
    fromDate=input('od: ')
    toDate=input('do: ')
    hash=input('hash: ')
    maksSati=LoadRadniSati()
    fromTS=datetime.timestamp(datetime.strptime(fromDate,"%d/%m/%Y"))
    toTS=datetime.timestamp(datetime.strptime(toDate,"%d/%m/%Y"))
    if connector.is_connected():
        query=f"select min(timestamp),max(timestamp) from res1.states where timestamp<={toTS} and timestamp>={fromTS} and hash='{hash}'" 
        cursor = connector.cursor()
        cursor.execute(query)
        print('Values:\n')
        for u in cursor:
            print(f"min:{u[0]}, max:{u[1]} ")
            print(u[1]-u[0])
    
#Menu
def Menu():
    while(True):
        print("1. Ispis uredjaja.")
        print("2. Broj radnih sati za uredjaj.")
        print("3. Prikaz vrednosti za period.Unesite datum pocetka i kraja perioda u formatu '20/1/2020'.")
        option=input()
        if(option=="1"):
            RetrieveAll()
        elif option=="2":
            BrojRadnihSati()
        elif option=="3":
            RetrieveAllByTime()
    return


def LoadTimeScale():
    with open('C:/Users/User/Desktop/FINALNORES/Res/time_config.xml') as fd:
        doc = xmltodict.parse(fd.read())
    return doc['timescale']['value']

def LoadTimeConfig():
    with open('C:/Users/User/Desktop/FINALNORES/Res/radnisaticonfig.xml') as fd:
        doc = xmltodict.parse(fd.read())
    return doc['timescale']['value']

if __name__ == "__main__":
    connector=mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="andrija")
    
    scaleTime=float(LoadTimeScale())
    timeConfig=float(LoadTimeScale())

    recieveProcess=Thread(target=ListenForMainControlerNotifications,args=())
    savechangesProcess = Thread(target=SaveChangesToDb,args=())
    menuProcess=Thread(target=Menu,args=())
    recieveProcess.start()
    menuProcess.start()
    savechangesProcess.start()