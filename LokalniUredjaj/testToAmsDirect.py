import unittest
import sys 
import os
import socket
sys.path.insert(0, "C:\\Users\\User\\Desktop\\FINALNORES\\Res\\LokalniUredjaj")
from main import ToAmsDirect
from LocalDevice import LocalDevice
from LocalDevice import DeviceType
from main import LoadTimeScale
import mock
from mock import patch
from mock import MagicMock
import pickle
devices = []



#@patch('main.ReportStateChanges')
class TestSlanje(unittest.TestCase):
    def test_case1(self):
        localDevice = LocalDevice(DeviceType.Digital,0,121212,"Andrija")
        timeScale =(LoadTimeScale())
        vrednost = ToAmsDirect(localDevice,timeScale)
        self.assertNotEqual(vrednost, 'ok' )
    
    def test_case2(self): #mock_reportstatechanges):
        localDevice = ""
        timeScale = float(LoadTimeScale())
        #devices.append[localDevice]
        #mock_reportstatechanges(devices, 5015)
        vrednost = ToAmsDirect(localDevice,timeScale)
        self.assertEqual(vrednost, "ERROR")
        #vrednost = ToAmsDirect(localDevice,timeScale)
        #self.assertEqual(vrednost, "ERROR")

    def test_case3(self): #mock_reportstatechanges):
        localDevice = LocalDevice(DeviceType.Analog,123,32,"Andrija")
        timeScale = ""
        #mock_reportstatechanges(devices, 5015)
        vrednost = ToAmsDirect(localDevice,timeScale)
        self.assertEqual(vrednost,"ERROR")
        #vrednost = ToAmsDirect(localDevice,timeScale)
        #self.assertNotEqual(vrednost,None)
    
    def test_case4(self): #mock_reportstatechanges):
        localDevice = LocalDevice(DeviceType.Analog,123,323,"Andrija")
        timeScale = ""
        #mock_reportstatechanges(devices, 5015)
        vrednost = ToAmsDirect(localDevice,timeScale)
        self.assertNotEqual(vrednost, None )
        #vrednost = ToAmsDirect(localDevice,timeScale)
        #self.assertEqual(vrednost, "ERROR")

if __name__ == '__main__':
    unittest.main()