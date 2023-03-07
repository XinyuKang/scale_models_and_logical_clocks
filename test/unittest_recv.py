import unittest
import threading
import time
from sa_test import Node
import socket

class TestNode(unittest.TestCase):

    def test_receive(self):
        try:
            node = Node(1, '127.0.0.1', 9005, [9004, 9006])
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(("localhost", 9005))
            print(client)
            message = "test message"
            client.send(message.encode("ascii"))

            time.sleep(1) # wait for message to be received

            self.assertEqual(len(node.message_queue), 1)
            self.assertEqual(node.message_queue[0], message)
            node.done = True
            node.stop()
            client.close()
            node.server.close()
            # assert no messages were received
            address = ('127.0.0.1', 9005)

        finally:
            client.close()
            node.server.close()

if __name__ == '__main__':
    unittest.main()