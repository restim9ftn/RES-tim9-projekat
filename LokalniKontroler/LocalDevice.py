from enum import Enum
from os import times
class DeviceType(Enum):
    Digital=0
    Analog=1
    
    

class LocalDevice:
    hash=""
    deviceType = DeviceType.Digital
    value=0
    timeStamp=0
    def __init__(self,type,value,timeStamp,hash):
        self.deviceType=type
        self.value=value
        self.timeStamp=timeStamp
        self.hash=hash

        
    def getHash(self):
        return self.hash
    def setHash(self,hash):
        self.hash=hash
        
    def getDeviceType(self):
        return self.deviceType  
    def setDeviceType(self,type):
        self.deviceType=type
        
    def getValue(self):
        return self.value
    def setValue(self,value):
        self.value=value
        
    def getTimeStamp(self):
        return self.timeStamp
    def setTimeStamp(self,timeStamp):
        self.timeStamp=timeStamp
        
    def getTypeString(self):
        if(self.deviceType==DeviceType.Digital):
            return "DIGITAL"
        else:   
            return "ANALOG"
    def toString(self):
        return f"Hash: {self.getHash()} Tip uredjaja: {self.getTypeString()}, Vrednost: {self.getValue()}, Poslednja izmena: {self.getTimeStamp()}"