from queue import Empty
from time import time
from types import NoneType
import unittest
import sys 
import os
sys.path.insert(0, "C:\\Users\\User\\Desktop\\FINALNORES\\Res\\LokalniUredjaj")
from main import Start
import main
from LocalDevice import LocalDevice
from LocalDevice import DeviceType
from main import LoadTimeScale
from main import ReportStateChanges
import mock
from mock import patch
from mock import MagicMock
import socket
import pickle
#localDevice1 = LocalDevice(DeviceType.Analog, 312, 13212231, "adsaa")
#localDevice2 = LocalDevice(DeviceType.Digital, 0, 123231, "asdds")
#localDevice3 = LocalDevice(DeviceType.Analog,132, 213231, "asdads")
#localDevice4 = LocalDevice(DeviceType.Digital, 1, 12231, "dasd")
#localDevice5 = LocalDevice(DeviceType.Analog, 555, 123231, "andrija")
devices = []
#devices.append[localDevice1]
#devices.append[localDevice2]
#devices.append[localDevice3]
#devices.append[localDevice4]
#devices.append[localDevice5]


class TestSlanje(unittest.TestCase):
    def test_case1(self):
        localDevice = LocalDevice(DeviceType.Digital,0,121212,"Andrija")
        timeScale =(LoadTimeScale())
        vrednost = Start(localDevice,timeScale)
        self.assertNotEqual(vrednost, 'ok' )
    
    def test_case2(self): #mock_reportstatechanges):
        localDevice = ""
        timeScale = float(LoadTimeScale())
        #devices.append[localDevice]
        #mock_reportstatechanges(devices, 5015)
        vrednost = Start(localDevice,timeScale)
        self.assertNotEqual(vrednost, "ERROR")
        #vrednost = ToAmsDirect(localDevice,timeScale)
        #self.assertEqual(vrednost, "ERROR")

    def test_case3(self): #mock_reportstatechanges):
        localDevice = LocalDevice(DeviceType.Analog,123,32,"Andrija")
        timeScale = ""
        #mock_reportstatechanges(devices, 5015)
        vrednost = Start(localDevice,timeScale)
        self.assertNotEqual(vrednost,"ERROR")
        #vrednost = ToAmsDirect(localDevice,timeScale)
        #self.assertNotEqual(vrednost,None)
    
    def test_case4(self): #mock_reportstatechanges):
        localDevice = LocalDevice(DeviceType.Analog,123,323,"Andrija")
        timeScale = ""
        #mock_reportstatechanges(devices, 5015)
        vrednost = Start(localDevice,timeScale)
        self.assertEqual(vrednost, None )
        #vrednost = ToAmsDirect(localDevice,timeScale)
        #self.assertEqual(vrednost, "ERROR")

if __name__ == '__main__':
    unittest.main()