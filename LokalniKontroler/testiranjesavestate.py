import unittest
import sys 
import os
from unittest.mock import MagicMock

sys.path.insert(0,"C:\\Users\\HP\\Downloads\\FINALNORES\\FINALNORES\\Res\\LokalniKontroler")
from main import ReadStateChanges
from main import SaveStateChanges
from main import ET
from LocalDevice import LocalDevice
from LocalDevice import DeviceType
import main
import socket
import pickle
import mock
from mock import patch

data = ET.Element('device')
items = ET.SubElement(data, 'device')


class MyTestCase1(unittest.TestCase):
    def test_case1(self):
        ET.SubElement(data,'device')
        value = SaveStateChanges()
        self.assertEqual(value,None)

    def test_case2(self):
        ET.SubElement(items, 'hash')
        value = SaveStateChanges()
        self.assertEqual(value, None)

    def test_case3(self):
        ET.SubElement(items, 'deviceType')
        value = SaveStateChanges()
        self.assertEqual(value, None)

    def test_case4(self):
        ET.SubElement(items, 'timeStamp')
        value = SaveStateChanges()
        self.assertEqual(value, None)

    def test_case5(self):
        ET.SubElement(items, 'value')
        value = SaveStateChanges()
        self.assertEqual(value, None)



if __name__ == '__main__':
    unittest.main()