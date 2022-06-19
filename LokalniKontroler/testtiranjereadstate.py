import unittest
import sys 
import os
from unittest.mock import MagicMock

sys.path.insert(0,"C:\\Users\\HP\\Downloads\\FINALNORES\\FINALNORES\\Res\\LokalniKontroler")
from main import ReadStateChanges

from main import ET
from LocalDevice import LocalDevice
from LocalDevice import DeviceType
import main
import socket
import pickle
import mock
from mock import patch

class MyTestCase(unittest.TestCase):
    def test_case1(self):
        localDevice = LocalDevice(DeviceType.Digital,1,12222,"Uros")
        vrednost = ReadStateChanges()
        self.assertEqual(vrednost,None)

    def test_case2(self):
        localDevice = ""
        vrednost = ReadStateChanges()
        self.assertEqual(vrednost,None)

    def test_case3(self):
        localDevice = LocalDevice(DeviceType.Analog,1,1223333,"Uros")
        vrednost = ReadStateChanges()
        self.assertEqual(vrednost,None)

    def test_case4(self):
        localDevice = LocalDevice(DeviceType.Analog,1,1223333,"Uros")
        vrednost = ReadStateChanges()
        self.assertEqual(vrednost,None)

if __name__ == '__main__':
    unittest.main()