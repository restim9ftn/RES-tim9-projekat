import pickle
import socket
import unittest
from unittest import mock
from LocalDevice import LocalDevice
import main
from unittest.mock import MagicMock, Mock, patch

 
tipuredjaja =["digital","analog"]
nizuredjaja=[]

class TestMeni(unittest.TestCase):
    
    def test_meni_ok(self):
        with mock.patch('builtins.input', return_value="1"):
            assert main.Menu(tipuredjaja,nizuredjaja) == 1
            
    def test_meni_van_opsega(self):
        with mock.patch('builtins.input', return_value="5"):
            assert main.Menu(tipuredjaja,nizuredjaja) == None
        with mock.patch('builtins.input', return_value="-3"):
            assert main.Menu(tipuredjaja,nizuredjaja) == None

    def test_meni_nije_broj(self):
        with mock.patch('builtins.input', return_value="test"):
            assert main.Menu(tipuredjaja,nizuredjaja) == None
        with mock.patch('builtins.input', return_value=[]):
            assert main.Menu(tipuredjaja,nizuredjaja) == None



if __name__ == "__main__":
    unittest.main()