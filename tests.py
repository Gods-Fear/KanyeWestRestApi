from unittest import TestCase
from unittest.mock import patch
from client import get_data, user_input, BASE_LINK_GET_DATA


class TestInput(TestCase):

    @patch('builtins.input', return_value=5)
    def test_answer_5(self, input):
        self.assertEqual(user_input(), 5)

    @patch('builtins.input', return_value=20)
    def test_answer_20(self, input):
        self.assertEqual(user_input(), 20)


class TestConnection(TestCase):

    def test_get_api(self):
        response = get_data(BASE_LINK_GET_DATA)
        self.assertEqual(type(response), str)
