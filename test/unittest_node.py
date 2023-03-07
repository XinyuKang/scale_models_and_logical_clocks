import unittest
import signal
from unittest.mock import patch, Mock
from sa_test import Node

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException('Test timed out')

class TestNode(unittest.TestCase):
    
    def setUp(self):
        self.port = 7002
        self.host = 'localhost'
        self.node = Node(id=1, host=self.host, port=self.port, port_list=[7002, 9002])
    
    @patch('socket.socket')
    def test_listen_method(self, mock_socket):
        #self.node = Node(id=1, host=self.host, port=self.port, port_list=[])
        # create a mock socket object
        mock_client_socket = Mock()
        mock_socket.return_value = mock_client_socket
        # create a mock message
        mock_message = "test message"
        # simulate incoming message
        self.node.message_queue.append(mock_message)
        self.assertEqual(self.node.message_queue, ['test message'])
        # call the listen() method
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.setitimer(signal.ITIMER_REAL, 2) # set timeout to 2 seconds
        try:
            self.node.listen()
            signal.alarm(0) # cancel the alarm
        except TimeoutException:
            self.fail('Test timed out')
        self.assertEqual(self.node.message_queue, ['test message'])
 
    @patch('socket.socket')
    def test_send(self, mock_socket):
        mock_client = mock_socket.return_value
        self.node.send(9002, 'test message1234')
        mock_client.connect.assert_called_with(('localhost', 9002))
        mock_client.send.assert_called_with(b'test message1234')
    
if __name__ == '__main__':
    unittest.main()



