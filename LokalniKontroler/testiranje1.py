import unittest
import sys 
import os
import main
from main import WriteDeviceToXml
from main import ET
from unittest.mock import MagicMock
sys.path.insert(0, "C:\\Users\\Nikola\\Desktop\\KRAJ\\RES-tim9-projekat\\LokalniKontroler")


data = ET.Element('devices')
items = ET.SubElement(data, 'device')

class MyTestCase(unittest.TestCase):
    
    def test_WriteDeviceToXml1(self):
        ET.SubElement(data, 'device')
        value = WriteDeviceToXml()
        self.assertEqual(value, None)
    
    def test_WriteDeviceToXml2(self):
        ET.SubElement(items, 'hash')
        value = WriteDeviceToXml()
        self.assertEqual(value, None)
    
    def test_WriteDeviceToXml3(self):
        ET.SubElement(items, 'deviceType')
        value = WriteDeviceToXml()
        self.assertEqual(value, None)
    
    def test_WriteDeviceToXml4(self):
        ET.SubElement(items, 'timeStamp')
        value = WriteDeviceToXml()
        self.assertEqual(value, None)

    def test_WriteDeviceToXml5(self):
        ET.SubElement(items, 'value')
        value = WriteDeviceToXml()
        self.assertEqual(value, None)


if __name__ == '__main__':
    unittest.main()
