from multiprocessing import Queue
import pickle
from random import randint
from re import S
import select
import socket
from threading import Thread
from dicttoxml import dicttoxml
import xmltodict
from xml.dom.minidom import parseString
from LocalDevice import LocalDevice
from LocalDevice import DeviceType
import time
from xml.dom import minidom
import xml.etree.ElementTree as ET

receivequeue=[]
devices=[]


def WriteDeviceToXml():
    data = ET.Element('devices')
    for d in devices:
        items = ET.SubElement(data, 'device')
        item2 = ET.SubElement(items, 'hash')
        item3 = ET.SubElement(items, 'deviceType')
        item4 = ET.SubElement(items, 'timStamp')
        item5 = ET.SubElement(items, 'value')
        item2.text = str(d.getHash())
        item3.text=str(d.getTypeString())
        item4.text=str(d.getTimeStamp())
        item5.text=str(d.getValue())
    ####
    mydata = ET.tostring(data)
    print("mydata",mydata)
    print("str(mydata)",str(mydata))
    #sklanjanje b' na pocetku i ' na kraju stringa
    mydata2 =str(mydata) 
    mydata2 = mydata2[2:len(mydata2)-1]
    print("mydata2",mydata2)
    myfile = open("devices.xml", "w")
    myfile.write(mydata2)
    return

def ReadDevicesFromXml():
    global devices
    mydoc = minidom.parse('devices.xml')
    devs = mydoc.getElementsByTagName('device')
    idx=0
    for i in range(0,len(devs)):
        devices.append(LocalDevice(0,"",0,""))
    for d in devs:
        br=0
        for c in d.childNodes:
            #print(c.firstChild.data)
            if(br==0):
                devices[idx].setHash(c.firstChild.data)
            elif(br==1):
                devices[idx].setDeviceType(c.firstChild.data)
            elif(br==2):
                devices[idx].setTimeStamp(c.firstChild.data)
            else:
                devices[idx].setValue(c.firstChild.data)
            br+=1
        idx+=1
    for i in range(0,len(devices)):
        print(devices[i].toString())
    return

def AddDevice(device):
    global devices
    ind=False
    for i in range(0,devices.count()):
        if(devices[i].getHash()==device.getHash()):
            ind=True
    if(ind):
        return False
    else:
        devices.append(device)
        WriteDeviceToXml(device)
        return True

def RegisterDevice():
    HOST=''
    PORT=5016
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    print ("Listening on port 5016 for new device registrations.")
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
                        device=pickle.loads(data)
                        if(AddDevice(device)):
                            s.send('ok'.encode())
                        else:
                            s.send('Device vec registrovan.'.encode())
                    else:
                        read_list.remove(s)
        except:
            print(readable)

def ReceiveStateChanges():
    global receivequeue 
    HOST=''
    PORT=5015
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    print ("Listening on port 5015 for new devices changes.")
    read_list = [ss]
    while True:
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is ss:
                client_socket, address = ss.accept()
                read_list.append(client_socket)
            else:
                data = s.recv(1024)
                if data:
                    update=pickle.loads(data)
                    update.toString()
                    receivequeue.append(update)
                    SaveStateChanges()
                    s.send('ok'.encode())    
                else:
                    s.close()

def SaveStateChanges():
    data = ET.Element('receivedchanges')
    for d in receivequeue:
        items = ET.SubElement(data, 'device')
        item1 = ET.SubElement(items, 'name')
        item2 = ET.SubElement(items, 'hash')
        item3 = ET.SubElement(items, 'deviceType')
        item4 = ET.SubElement(items, 'timStamp')
        item5 = ET.SubElement(items, 'value')
        item1.text = str(d.getName())
        item2.text = str(d.getHash())
        item3.text=str(d.getTypeString())
        item4.text=str(d.getTimeStamp())
        item5.text=str(d.getValue())
    
    mydata = ET.tostring(data)
    print("mydata",mydata)
    print("str(mydata)",str(mydata))
    #sklanjanje b' na pocetku i ' na kraju stringa
    mydata2 =str(mydata) 
    mydata2 = mydata2[2:len(mydata2)-1]
    print("mydata2",mydata2)
    myfile = open("receivedchanges.xml", "w")
    myfile.write(mydata2)
    return
        
def ReadStateChanges():
    mydoc = minidom.parse('receivedchanges.xml')
    devs = mydoc.getElementsByTagName('device')
    idx=0
    for i in range(0,len(devs)):
        receivequeue.append(LocalDevice("","","","",""))
    for d in devs:
        br=0
        for c in d.childNodes:
            #print(c.firstChild.data)
            if(br==0):
                #print(c.firstChild.data)
                devices[idx].setName(c.firstChild.data)
            elif(br==1):
                devices[idx].setHash(c.firstChild.data)
            elif(br==2):
                devices[idx].setDeviceType(c.firstChild.data)
            elif(br==3):
                devices[idx].setValue(c.firstChild.data)
            else:
                devices[idx].setTimeStamp(c.firstChild.data)
            br+=1
        idx+=1
    for i in range(0,len(devices)):
        print(devices[i].toString())
    return

def ClearReceivedChanges():
    myfile = open("receivedchanges.xml", "w")
    myfile.write("")

def PassStateChangesToAMS(timeScale):
    while(1):
        time.sleep(60*5*timeScale)
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5017
        MESSAGE = pickle.dumps(receivequeue)
        #trebalo bi ovdje
        receivequeue.clear()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        response=s.recv(1024)
        print(response.decode())
        if(response.decode()=='ok'):
            print("Uspjesno poslati podaci ka AMS")
            ClearReceivedChanges()
        else:
            print("Neuspjesno slanje ka AMS")
            ReadStateChanges()
        s.close()

    return

def LoadTime():
    with open('./time_config.xml') as fd:
        doc = xmltodict.parse(fd.read())
    return doc['timescale']['value']




if __name__=="__main__":
    input('started')
    timeScale=float(LoadTime())
    ReadDevicesFromXml()
    recieveProcess=Thread(target=ReceiveStateChanges,args=())
    sendProces=Thread(target=SaveStateChanges,args=())
    saveProcess=Thread(target=PassStateChangesToAMS,args=[timeScale])
    registerProcess = Thread(target=RegisterDevice,args=())
    recieveProcess.start()
    sendProces.start()
    saveProcess.start()
    registerProcess.start()
    WriteDeviceToXml()
    input("Program working...")