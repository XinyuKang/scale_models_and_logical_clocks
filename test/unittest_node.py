import unittest
import signal
from unittest.mock import patch, Mock
from sa_test import Node
import random
import datetime

run = 5
seconds = 2


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException('Test timed out')


class TestNode(unittest.TestCase):

    def setUp(self):
        self.port = 7003
        self.host = 'localhost'
        self.node = Node(id=1, host=self.host, port=self.port,
                         port_list=[7003, 9000])

    @patch('socket.socket')
    def test_listen_method(self, mock_socket):
        # self.node = Node(id=1, host=self.host, port=self.port, port_list=[])
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
        signal.setitimer(signal.ITIMER_REAL, 2)  # set timeout to 2 seconds
        try:
            self.node.listen()
            signal.alarm(0)  # cancel the alarm
        except TimeoutException:
            self.fail('Test timed out')
        self.assertEqual(self.node.message_queue, ['test message'])

    @patch('socket.socket')
    def test_send(self, mock_socket):
        mock_client = mock_socket.return_value
        self.node.send(9002, 'test message1234')
        mock_client.connect.assert_called_with(('localhost', 9002))
        mock_client.send.assert_called_with(b'test message1234')

    @patch('socket.socket')
    def test_cycle_action(self, seconds, run):
        receiver_id_1 = (self.node.id+1) % 3
        receiver_id_2 = (self.node.id+2) % 3
        message = f"'Machine {self.node.id} has logical clock time {self.node.logical_clock}'"
        rand = random.randint(1, 10)
        for _ in range(seconds):
            for i in range(run):
                if rand == 1:
                    self.node.send(self.node.port_list[receiver_id_1], message)
                    # update the log with the send
                    tept_message = f"SENT(rand=1): {message} TO MACHINE #{receiver_id_1} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
                    self.node.logger.info(tept_message)
                    assert self.node.logger.info == f"SENT(rand=1): {message} TO MACHINE #{receiver_id_1} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
                if rand == 2:
                    self.node.send(self.node.port_list[receiver_id_2], message)
                    tept_message = f"SENT(rand=2): {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
                    self.node.logger.info(tept_message)
                    assert self.node.logger.info == f"SENT(rand=2): {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
                if rand == 3:
                    self.node.send(self.node.port_list[receiver_id_1], message)
                    self.node.send(self.node.port_list[receiver_id_2], message)
                    tept_message = f"SENT(rand=3): {message} TO MACHINE #{receiver_id_1} and #{receiver_id_2} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.logical_clock}"
                    self.node.logger.info(tept_message)
                    assert self.node.logger.info == f"SENT(rand=3): {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
                self.node.logical_clock += 1


if __name__ == '__main__':
    unittest.main()
