import unittest
from unittest.mock import patch, Mock
from sa_test import Node
import random
import datetime


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException('Test timed out')


class TestNode(unittest.TestCase):

    def setUp(self):
        self.port = 7002
        self.host = 'localhost'
        self.node = Node(id=1, host=self.host, port=self.port,
                         port_list=[7002, 9002])

    # test update log and send message in one cycle.
    def test_cycle_action(self):
        receiver_id_1 = (self.node.id+1) % 3
        receiver_id_2 = (self.node.id+2) % 3
        message = f"'Machine {self.node.id} has logical clock time {self.node.logical_clock}'"
        rand = random.randint(1, 10)
        if rand == 1:
            self.node.send(self.node.port_list[receiver_id_1], message)
            # update the log with the send
            tept_message = f"SENT(rand=1): {message} TO MACHINE #{receiver_id_1} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
            self.node.logger.info(tept_message)
            print(self.node.logger.info)
            assert self.node.logger.info == f"SENT(rand=1): {message} TO MACHINE #{receiver_id_1} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
            self.node.logical_clock.add()
        if rand == 2:
            self.node.send(self.node.port_list[receiver_id_2], message)
            tept_message = f"SENT(rand=2): {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
            self.node.logger.info(tept_message)
            print(self.node.logger.info)
            assert self.node.logger.info == f"SENT(rand=2): {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
            self.node.logical_clock.add()
        if rand == 3:
            self.node.send(self.node.port_list[receiver_id_1], message)
            self.node.send(self.node.port_list[receiver_id_2], message)
            tept_message = f"SENT(rand=3): {message} TO MACHINE #{receiver_id_1} and #{receiver_id_2} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.logical_clock}"
            self.node.logger.info(tept_message)
            print(self.node.logger.info)
            assert self.node.logger.info == f"SENT(rand=3): {message} TO MACHINE #{receiver_id_2} - GLOBAL TIME: {datetime.datetime.now()} - LOGICAL CLOCK TIME: {self.node.logical_clock}"
            self.node.logical_clock.add()


if __name__ == '__main__':
    unittest.main()
