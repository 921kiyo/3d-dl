import unittest
import requests
from requests.exceptions import MissingSchema

from ..SlackReporter import *

class TestSlack(unittest.TestCase):
    """
    Run tests for SlackReporter
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_plain_setup(self):
        slack = SlackReporter(webhook_url='http://nothing', disable=True)
        self.assertFalse(slack is None)

    def test_setup_disable(self):

        slack = SlackReporter(webhook_url='http://nothing', disable=True)
        slack.send_message('test', print_message=True)
        self.assertTrue(slack.disable is True)

    def test_plain_setup(self):
        slack = SlackReporter(webhook_url='http://nothing', disable=True)
        slack.send_message('test', print_message=False)

    def test_print_message(self):
        slack = SlackReporter(webhook_url='http://nothing', disable=True)
        slack.send_message('test', print_message=False)

    def test_valid_url(self):
        slack = SlackReporter(webhook_url='https://slack.com/api/api.test', disable=False)
        slack.send_message('test', print_message=True)

    def test_valid_url(self):
        slack = SlackReporter(webhook_url='https://slack.com/api/api.nope', disable=False)
        slack.send_message('test', print_message=True)











if __name__ == '__main__':

    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSlack)
    success = unittest.TextTestRunner().run(suite).wasSuccessful()

