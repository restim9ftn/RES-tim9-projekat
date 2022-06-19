import unittest
import sys 
import os
from unittest.mock import MagicMock
sys.path.insert(0, "C:\\Users\\User\\Desktop\\FINALNORES\\Res\\LokalniUredjaj")
from main import TurnOff
from LocalDevice import LocalDevice
from LocalDevice import DeviceType
import socket
import pickle 
import mock
from mock import patch


class TestSlanje(unittest.TestCase):
    @patch('main.TurnOff')
    def test_slanje_ok(self, mock_turnoff):
        localDevice = LocalDevice(DeviceType.Digital,1,121212,"Andrija")
        mock_socket = MagicMock(socket.socket)
        MESSAGE = pickle.dumps(localDevice)
        mock_socket.recv = MagicMock(return_value = MESSAGE)
        mock_turnoff.return_value = mock_socket
        self.assertNotEqual(TurnOff(),"ERROR")
        
    @patch('main.TurnOff')
    def test_slanje_error(self, mock_turnoff):
        localDevice = LocalDevice(DeviceType.Digital,1,121212,"Andrija")
        mock_socket = MagicMock()
        MESSAGE = pickle.dumps(localDevice)
        mock_socket.send.side_effect = socket.error
        mock_turnoff.return_value = mock_socket
        self.assertNotEqual(TurnOff(), "ERROR")
    
    @patch('main.TurnOff')
    def test_slanje_ok1(self, mock_turnoff):
        localDevice = LocalDevice(DeviceType.Digital,1,121212,"Andrija")
        mock_socket = MagicMock()
        MESSAGE = pickle.dumps("")
        mock_socket.recv = MagicMock(return_value = MESSAGE)
        mock_turnoff.return_value = mock_socket
        self.assertEqual(TurnOff(), None)

    
    @patch('main.TurnOff')
    def test_slanje_error1(self, mock_turnoff):
        localDevice = LocalDevice(DeviceType.Digital,1,121212,"Andrija")
        mock_socket = MagicMock()
        mock_socket.send.side_effect = socket.error
        mock_turnoff.return_value = mock_socket
        self.assertNotEqual(TurnOff(), "ERROR")

if __name__ == '__main__':
    unittest.main()