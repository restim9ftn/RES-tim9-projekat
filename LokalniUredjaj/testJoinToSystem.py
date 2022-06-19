import unittest
import sys 
import os
from unittest.mock import MagicMock
sys.path.insert(0, "C:\\Users\\User\\Desktop\\FINALNORES\\Res\\LokalniUredjaj")
from main import JoinToSystem
from LocalDevice import LocalDevice
from LocalDevice import DeviceType
import socket
import pickle 
import mock
from mock import patch

TCP_IP = '127.0.0.1'
TCP_PORT = 5016

class TestSlanje(unittest.TestCase):
    @patch('main.JoinToSystem')
    def test_slanje_ok(self, mock_join):
        localDevice = LocalDevice(DeviceType.Digital,1,121212,"Andrija")
        mock_socket = MagicMock(socket.socket)
        MESSAGE = pickle.dumps(localDevice)
        mock_socket.send = MagicMock(return_value = MESSAGE)
        mock_socket.recv = MagicMock(return_value = 'ok')
        mock_join.return_value = mock_socket
        self.assertNotEqual(JoinToSystem(localDevice),"Uspesno prikljucenje kao novi uredjaj:",localDevice.toString())
        
    @patch('main.JoinToSystem')
    def test_slanje_error(self, mock_join):
        localDevice = LocalDevice(DeviceType.Digital,1,121212,"Andrija")
        mock_socket = MagicMock()
        MESSAGE = pickle.dumps(localDevice)
        mock_socket.send.side_effect = socket.error
        mock_join.return_value = mock_socket
        self.assertEqual(JoinToSystem(localDevice), "ERROR")
    
    @patch('main.JoinToSystem')
    def test_slanje_ok1(self, mock_join):
        localDevice = LocalDevice(DeviceType.Digital,1,121212,"Andrija")
        mock_socket = MagicMock()
        MESSAGE = pickle.dumps("")
        mock_socket.send = MagicMock(return_value = MESSAGE)
        mock_socket.recv = MagicMock(return_value = 'ok')
        mock_join.return_value = mock_socket
        self.assertNotEqual(JoinToSystem(localDevice), "Uspesno prikljucenje kao novi uredjaj:",localDevice.toString())

    
    @patch('main.JoinToSystem')
    def test_slanje_error1(self, mock_join):
        localDevice = LocalDevice(DeviceType.Digital,1,121212,"Andrija")
        mock_socket = MagicMock()
        mock_socket.send.side_effect = socket.error
        mock_join.return_value = mock_socket
        self.assertEqual(JoinToSystem(localDevice), "ERROR")

if __name__ == '__main__':
    unittest.main()