import unittest
import signal
from unittest.mock import patch, Mock
import os
import tempfile
from sa_test import Node
import logging

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException('Test timed out')

class TestNode(unittest.TestCase):
    def setUp(self):
        self.port = 7001
        self.host = 'localhost'
        self.node = Node(id=1, host=self.host, port=self.port, port_list=[])
    
    def test_set_log(self):
        # Create a temporary log file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.close()

            # Create a node and set its log to the temporary file
            node = Node(1, '127.0.0.1', 1234, [])
            #node = self.node
            node.set_log(temp_file.name, "test_logger")

            # Check that the log file was created and the logger was set up correctly
            self.assertIsInstance(node.logger, logging.Logger)
            self.assertTrue(os.path.isfile(temp_file.name))
            self.assertEqual(node.logger.name, "test_logger")
            self.assertEqual(node.logger.handlers[0].baseFilename, temp_file.name)
            self.assertIsInstance(node.logger.handlers[0], logging.FileHandler)
            self.assertEqual(node.logger.level, logging.INFO)
            # Write a log message and verify that it was written to the log file
            node.logger.info("test message")
            with open(temp_file.name) as f:
                content = f.read()
            self.assertIn("test message", content)

            # Clean up by deleting the log file
            os.unlink(temp_file.name)
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, 1) # set timeout to 5 seconds
            try:
                print("test log")
                signal.alarm(0) # cancel the alarm
            except TimeoutException:
                self.fail('Test timed out')
        
if __name__ == '__main__':
    unittest.main()



