from multiprocessing import Queue
import pickle
from re import S
import select
import socket
from threading import Thread
from dicttoxml import dicttoxml
import xmltodict
from xml.dom.minidom import parseString
import LocalDevice
from xml.dom import minidom
import xml.etree.ElementTree as ET

receivequeue=Queue()
devices=[]


def WriteDeviceToXml():
    devices.append(LocalDevice.LocalDevice(LocalDevice.DeviceType.Digital,0,0,"dfg","sdf"))
    devices.append(LocalDevice.LocalDevice(LocalDevice.DeviceType.Digital,0,0,"hhh","hhh"))
    #d=LocalDevice.LocalDevice(LocalDevice.DeviceType.Digital,0,0,"","")
    
    data = ET.Element('devices')
    for d in devices:
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
    ####
    # create the file structure
   
    

    # create a new XML file with the results
    mydata = ET.tostring(data)
    myfile = open("devices.xml", "w")
    myfile.write(str(mydata))
    return
def ReadDevicesFromXml():
    # parse an xml file by name
    mydoc = minidom.parse('devices.xml')

    devices = mydoc.getElementsByTagName('device')
    for d in devices:
        for c in d.childNodes:
            print(c.firstChild.data)
    # one specific item attribute
    # print('Item #2 attribute:')
    # print(items[1].attributes['name'].value)

    # # all item attributes
    # print('\nAll attributes:')
    # for elem in items:
    #     print(elem.attributes['name'].value)

    # # one specific item's data
    # print('\nItem #2 data:')
    # print(items[1].firstChild.data)
    # print(items[1].childNodes[0].data)

    # # all items data
    # print('\nAll item data:')
    # for elem in items:
    #     print(elem.firstChild.data)
    return
def AddDevice(device):
    global devices
    ind=False
    for i in range(0,devices.count()):
        if(devices[i].getHash()==device.getHash()):
            ind=True
    if(ind):
        return
    else:
        WriteDeviceToXml(device)
        devices.append(device)

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
                        AddDevice(device)
                        s.send('ok'.encode()) 
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
                    receivequeue.put(update)
                    s.send('ok'.encode())    
                else:
                    s.close()

def SaveStateChanges():
    global receivequeue
    while(True):
        changes = receivequeue.get()
        

    
def PassStateChangesToAMS():
    return

def LoadTime():
    with open('./time_config.xml') as fd:
        doc = xmltodict.parse(fd.read())
    return doc['timescale']['value']


def LoadDevices():
    global devices
    #ucitati ih iz xml

if __name__=="__main__":
    # LoadDevices()
    # recieveProcess=Thread(target=ReceiveStateChanges,args=())
    # sendProces=Thread(target=SaveStateChanges,args=())
    # saveProcess=Thread(target=PassStateChangesToAMS,args=())
    # registerProcess = Thread(target=RegisterDevice,args=())
    # recieveProcess.Start()
    # sendProces.Start()
    # saveProcess.Start()
    # registerProcess.Start()
    #WriteDeviceToXml()
    ReadDevicesFromXml()
    input("Program working...")