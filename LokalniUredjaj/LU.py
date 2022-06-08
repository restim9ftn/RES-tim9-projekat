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

def ReportStateChanges(localDevice): #menjanje stanja
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5015
    MESSAGE = pickle.dumps(localDevice)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    response=s.recv(1024)
    print(response.decode())
    if(response.decode()=='ok'):
        print("Uspesno javljeno o promenama uredjaja:",localDevice.toString())
    else:
        print("Neuspesno javljeno o promenama uredjaja:",localDevice.toString())
    s.close()

def JoinToSystem(localDevice):
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5016
    MESSAGE = pickle.dumps(localDevice)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    response=s.recv(1024)
    print(response.decode())
    if(response.decode()=='ok'):
        print("Uspesno prikljucenje kao novi uredjaj:",localDevice.toString())
    else:
        print("Vec postoji kao uredjaj u sistemu:",localDevice.toString())
    s.close()
   

def LoadTimeScale():

    with open('./time_config.xml') as fd:
        doc = xmltodict.parse(fd.read())
    return doc['timescale']['value']


if __name__ == '__main__':
    #ovde pokupimo patrametre iz aplikacije koja startuje
    #users = sys.argv[2:len(sys.argv)]
    #username=users[int(sys.argv[1])]
    scaleTime=LoadTimeScale()
    localDevice = LocalDevice(DeviceType.Digital,0,time.time())
    JoinToSystem(localDevice)
    #Start(localDevice,scaleTime) #time scale treba uvesti iz xml