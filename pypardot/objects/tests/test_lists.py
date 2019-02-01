import unittest
import pprint

from pypardot.client import PardotAPI
from pypardot.errors import PardotAPIArgumentError, PardotAPIError

try:
	from pypardot.objects.tests.config import *

	CONFIG_EXISTS = True
except SystemError as e:
	CONFIG_EXISTS = False


@unittest.skipUnless(CONFIG_EXISTS, 'Requires Pardot configuration in config.py')
class TestLists(unittest.TestCase):
	def setUp(self):
		self.pardot = PardotAPI(email=PARDOT_USER, password=PARDOT_PASSWORD, user_key=PARDOT_USER_KEY)
		self.pardot.authenticate()

		self.email_address = 'parrot@harbles.com'
		self.test_list = 'Internal Test List'

	def tearDown(self):
		pass

	def test_list_read(self):
		results = self.pardot.lists.read(id=611)
		pprint.pprint(results)
		self.assertTrue(False)