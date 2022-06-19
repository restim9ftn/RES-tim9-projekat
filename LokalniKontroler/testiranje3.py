import unittest
import sys 
import os
import main
from main import AddDevice
from main import WriteDeviceToXml
from main import LocalDevice
from LocalDevice import DeviceType
from unittest.mock import MagicMock
sys.path.insert(0, "C:\\Users\\Nikola\\Desktop\\KRAJ\\RES-tim9-projekat\\LokalniKontroler")




ind = False

class MyTestCase(unittest.TestCase):
    def test_AddDevice(self):
        device = LocalDevice(DeviceType.Digital, 1, 37472, "")
        vrednost = AddDevice(device)
        self.assertEqual(vrednost, True)

    def test_AddDevice2(self):
        device = LocalDevice(DeviceType.Analog, 15347, 37472, "")
        vrednost = AddDevice(device)
        self.assertEqual(vrednost, False)

if __name__ == '__main__':
    unittest.main()