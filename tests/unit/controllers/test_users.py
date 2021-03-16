import unittest
from core.controllers.user import User as Controller
from core.models.user import User as UserModel
from mock import patch, Mock
from werkzeug.exceptions import BadRequest, NotFound


class TestUsersController(unittest.TestCase):
    def setUp(self):
        self.class_under_test = Controller()

    @patch.object(UserModel, 'query')
    def test_should_get_one(self, mock_user_get):
        user = UserModel()
        user.username = "Foo"
        user.id = '12'
        mock_user_get.get.return_value = user

        expected = {'id': '12', 'username': 'Foo'}
        self.assertEqual(expected, self.class_under_test.get(12))

    @patch.object(UserModel, 'query')
    def test_should_return_about404_user_notfound(self, mock_user_get):
        mock_user_get.get.return_value = None
        with self.assertRaises(NotFound) as context:
            self.class_under_test.get(12)
        self.assertIn('404 Not Found', str(context.exception))

    def test_should_return_about404_user_notfound_params_when_post(self):
        with self.assertRaises(BadRequest) as context:
            self.class_under_test.post(None, None)
        self.assertIn('400 Bad Request', str(context.exception))

        with self.assertRaises(BadRequest) as context:
            self.class_under_test.post('foo', None)
        self.assertIn('400 Bad Request', str(context.exception))

        with self.assertRaises(BadRequest) as context:
            self.class_under_test.post(None, 'bar')
        self.assertIn('400 Bad Request', str(context.exception))

    @patch.object(UserModel, 'query')
    def test_should_return_about404_user_exist_when_post(self, mock_user_get):
        user = UserModel()
        user.username = "Foo"
        user.id = 12
        mock_user_get.filter.first.return_value = user
        with self.assertRaises(BadRequest) as context:
            self.class_under_test.post('foo', 'bar')
        self.assertIn('400 Bad Request', str(context.exception))

    # @patch('core.models.user.User')
    @patch.object(UserModel, 'save')
    @patch('core.models.user.User.query')
    def test_should_post_record(self, mock_user_get, mock_user_save):
        mock_user_get.filter('username' == 'foo').first.return_value = None
        self.class_under_test.post('foo', 'bar')
        mock_user_save.return_value = True
        self.assertTrue(mock_user_save.called)
