import unittest
from sa_test import LogicalClock


class TestLogicalClock(unittest.TestCase):

    def test_update_method(self):
        clock1 = LogicalClock(10)
        clock2 = LogicalClock(20)
        clock1.update(clock2.get_time())
        self.assertEqual(clock1.get_time(), 21)

    def test_add_method(self):
        clock = LogicalClock()
        initial_time = clock.get_time()
        clock.add()
        new_time = clock.get_time()
        self.assertEqual(new_time, initial_time + 1)

    def test_get_time_method(self):
        clock = LogicalClock(5)
        self.assertEqual(clock.get_time(), 5)


if __name__ == '__main__':
    unittest.main()
