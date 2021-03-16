import unittest
from core.models.user import User as UserModel
from mock import patch, Mock
from passlib.apps import custom_app_context as pwd_context


class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.class_under_test = UserModel()

    @patch('core.models.user.User')
    def test_should_get_all(self, mock_user_get_all):
        user = UserModel()
        user.username = "Foo"
        user.id = 12
        mock_user_get_all.query.all.return_value = [user]

        users = self.class_under_test.get_all()
        self.assertEqual(1, len(users))

        user = users[0]
        self.assertEqual(12, user.id)
        self.assertEqual('Foo', user.username)

    def test_should_verify_password(self):
        password = 'foobar';
        self.class_under_test.hash_password(password)
        self.assertTrue(self.class_under_test.verify_password(password))

    @patch('core.db.session.commit', return_value=None)
    @patch('core.db.session.add', return_value=None)
    def test_save(self, mock_add, mock_commit):
        user = UserModel()
        user.username = "Foo"
        user.id = 12

        user.save()

    # def test_should_generate_auth_token(self):
    #     password = 'foobar';
    #     self.assertEqual('dsa', self.class_under_test.generate_auth_token(password))
