import unittest
import sys 
import os
import main
from main import ReadDevicesFromXml
from main import LocalDevice
from LocalDevice import DeviceType

from unittest.mock import MagicMock
sys.path.insert(0, "C:\\Users\\Nikola\\Desktop\\KRAJ\\RES-tim9-projekat\\LokalniKontroler")


class MyTestCase(unittest.TestCase):
    def test_case1(self):
        localDevice = LocalDevice(DeviceType.Digital,1,13622,"Nikola")
        vrednost = ReadDevicesFromXml()
        self.assertEqual(vrednost,None)

    def test_case2(self):
        localDevice = ""
        vrednost = ReadDevicesFromXml()
        self.assertEqual(vrednost, None)

    def test_case3(self):
        localDevice = LocalDevice(DeviceType.Analog,1,1223333,"Nikola")
        vrednost = ReadDevicesFromXml()
        self.assertEqual(vrednost,None)

    def test_case4(self):
        localDevice = LocalDevice(DeviceType.Analog,1,1223333,"Nikola")
        vrednost = ReadDevicesFromXml()
        self.assertEqual(vrednost, None)

if __name__ == '__main__':
    unittest.main()