import unittest
from core.controllers.ping import Ping
from werkzeug.exceptions import HTTPException, NotFound


class PingTest(unittest.TestCase):
    def setUp(self):
        self.class_under_test = Ping()

    def test_should_return_one(self):
        expected = ({'id': 1, 'response': 'Ping 1'}, 200)
        self.assertEqual(expected, self.class_under_test.get(1))

    def test_should_return_all(self):
        expected = ({1: 'Ping 1', 2: 'Ping 2', 3: 'Ping 3'}, 200)
        self.assertEqual(expected, self.class_under_test.get())

    def test_should_about404_ping_notfound(self):
        with self.assertRaises(NotFound) as context:
            self.class_under_test.abort_if_ping_doesnt_exist(32)
        self.assertIn('404 Not Found', str(context.exception))

    def test_should_z_delete_and_return_204(self):
        expected = ('', 204)
        self.assertEqual(expected, self.class_under_test.delete(3))
