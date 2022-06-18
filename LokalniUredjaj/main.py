import pickle
import socket
from threading import local
from LocalDevice import LocalDevice,DeviceType
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
import os 
import xml.etree.ElementTree as gfg 
from random import randint
from time import sleep
from dicttoxml import dicttoxml
import xmltodict
import select
import socket
import sys

terminate=False


def ReportStateChanges(localDevice,port): #funkcija promene
    TCP_IP = '127.0.0.1'
    TCP_PORT = port #5015
    MESSAGE = pickle.dumps(localDevice)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    
    s.send(MESSAGE)
    # try:
    #    response=s.recv(1024)
    # except Exception as e:
    #     print("exception")
    #     input(e)
    # print(response.decode())
    #if(response.decode()=='ok'):
    #    print("Uspesno javljeno o promenama uredjaja:",localDevice.toString())
    #else:
    #    print("Neuspesno javljeno o promenama uredjaja:",localDevice.toString())
    #s.close()

def JoinToSystem(localDevice):
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5016
    MESSAGE = pickle.dumps(localDevice)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    print("Send message reg: ",MESSAGE)

    response=s.recv(1024)
    print(response.decode())
    if(response.decode()=='ok'):
        print("Uspesno prikljucenje kao novi uredjaj:",localDevice.toString())
    else:
        print(response.decode(),localDevice.toString())
    s.close()

def TurnOff():
    HOST=''
    PORT=5555
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    print ("Listening on port 5555 for new device registrations.")
    read_list = [ss]
    while True:
        try:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is ss:
                    client_socket, address = ss.accept()
                    read_list.append(client_socket)
                    print( "Connection from", address)
                else:
                    data = s.recv(8192)
                    if data:
                        command=pickle.loads(data)
                        if(command=='ugasi'):
                            terminate=True
                    else:
                        read_list.remove(s)
        except:
            print(readable)

def Start(localDevice,timeScale):
    while(terminate == False):
        print('SENDING TO LOCAL CONTROLLER')
        try:
            sleep(randint(90,100)*timeScale)
        except Exception as e:
            input(e)
        oldVal = localDevice.getValue()
        if(localDevice.getDeviceType()==DeviceType.Digital):
            localDevice.setValue(randint(0,1))
            localDevice.setTimeStamp(time.time())
            if(oldVal!=localDevice.getValue()):
                ReportStateChanges(localDevice,5015)
                print("Stara vrednost:",oldVal,"Nova vrednost:",localDevice.getValue(),"Timestamp:",localDevice.getTimeStamp())
            else:
                print("Nije doslo do promena","Stara vrednost:",oldVal,"Nova vrednost:",localDevice.getValue(),"Timestamp:",localDevice.getTimeStamp())             
        else:
            localDevice.setValue(randint(0,1000))
            localDevice.setTimeStamp(time.time())
            if(oldVal!=localDevice.getValue()):
                ReportStateChanges(localDevice,5015)
                print("Stara vrednost:",oldVal,"Nova vrednost:",localDevice.getValue(),"Timestamp:",localDevice.getTimeStamp())
            else:
                print("Nije doslo do promena","Stara vrednost:",oldVal,"Nova vrednost:",localDevice.getValue(),"Timestamp:",localDevice.getTimeStamp())             

def ToAmsDirect(localDevice,timeScale):
    while(terminate==False):
        print("SENDING TO AMS")
        try:
            sleep(randint(90,100)*timeScale)
        except Exception as e:
            input(e)
        oldVal = localDevice.getValue()
        if(localDevice.getDeviceType()==DeviceType.Digital):
            localDevice.setValue(randint(0,1))
            localDevice.setTimeStamp(time.time())
            if(oldVal!=localDevice.getValue()):
                devices=[localDevice]
                ReportStateChanges(devices,5017)
                print("Stara vrednost:",oldVal,"Nova vrednost:",localDevice.getValue(),"Timestamp:",localDevice.getTimeStamp())
            else:
                print("Nije doslo do promena","Stara vrednost:",oldVal,"Nova vrednost:",localDevice.getValue(),"Timestamp:",localDevice.getTimeStamp())             
        else:
            localDevice.setValue(randint(0,1000))
            localDevice.setTimeStamp(time.time())
            if(oldVal!=localDevice.getValue()):
                devices=[localDevice]
                ReportStateChanges(devices,5017)
                print("Stara vrednost:",oldVal,"Nova vrednost:",localDevice.getValue(),"Timestamp:",localDevice.getTimeStamp())
            else:
                print("Nije doslo do promena","Stara vrednost:",oldVal,"Nova vrednost:",localDevice.getValue(),"Timestamp:",localDevice.getTimeStamp())             
               

def LoadTimeScale():
    with open('./time_config.xml') as fd:
        doc = xmltodict.parse(fd.read())
    return doc['timescale']['value']


if __name__ == '__main__':#parametri za uredjaj od monitoringa -> type,value,timeStamp,hash
    #ovde pokupimo patrametre iz aplikacije koja startuje
    #localDevice = LocalDevice(DeviceType(int('0')),int('1'),float('1.345'),'wsedrftghasdfg')
    dev_type = sys.argv[1]
    dev_value = sys.argv[2]
    dev_timestamp = sys.argv[3]
    dev_hash = sys.argv[4]
    mode=sys.argv[5]
    scaleTime=float(LoadTimeScale())
    localDevice = LocalDevice(DeviceType(int(dev_type)),int(dev_value),float(dev_timestamp),dev_hash)
    print(localDevice.toString())
    if mode == 'ams':
        ToAmsDirect(localDevice, scaleTime)
    else:
        JoinToSystem(localDevice)
        Start(localDevice,scaleTime) #time scale treba uvesti iz xml