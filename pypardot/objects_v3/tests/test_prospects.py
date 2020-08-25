import unittest

from pypardot.client import PardotAPI
from pypardot.errors import PardotAPIArgumentError, PardotAPIError

try:
    from pypardot.objects.tests.config import *
    CONFIG_EXISTS = True
except SystemError as e:
    CONFIG_EXISTS = False


@unittest.skipUnless(CONFIG_EXISTS, 'Requires Pardot configuration in config.py')
class TestProspects(unittest.TestCase):
    def setUp(self):
        self.pardot = PardotAPI(email=PARDOT_USER, password=PARDOT_PASSWORD, user_key=PARDOT_USER_KEY)
        self.pardot.authenticate()

        self.email_address = 'parrot@harbles.com'
        self.first_name = 'Pickles'
        self.last_name = 'Zardnif'

        # Make sure there isn't an existing prospect in the test account.
        try:
            self.pardot.prospects.delete_by_email(email=self.email_address)
        except PardotAPIError as e:
            # Error code 4 is raised if the prospect doesn't exist.
            if e.err_code != 4:
                raise e

    def tearDown(self):
        try:
            self.pardot.prospects.delete_by_email(email=self.email_address)
        except PardotAPIError as e:
            # Error code 4 is raised if the prospect doesn't exist.
            if e.err_code != 4:
                raise e

    def _check_prospect(self, prospect):
        self.assertEquals(self.email_address, prospect['email'])
        self.assertEquals(self.first_name, prospect['first_name'])
        self.assertEquals(self.last_name, prospect['last_name'])

    def test_create_and_read(self):
        with self.assertRaises(PardotAPIArgumentError):
            results = self.pardot.prospects.create_by_email(first_name=self.first_name, last_name=self.last_name)

        results = self.pardot.prospects.create_by_email(email=self.email_address, first_name=self.first_name, last_name=self.last_name)

        prospect = results['prospect']
        self._check_prospect(prospect)

        with self.assertRaises(PardotAPIArgumentError):
            results = self.pardot.prospects.read_by_id(email='test@test.com')

        results = self.pardot.prospects.read_by_id(id=prospect['id'])
        self._check_prospect(results['prospect'])

        with self.assertRaises(PardotAPIArgumentError):
            results = self.pardot.prospects.read_by_email(id='test')

        results = self.pardot.prospects.read_by_email(email=prospect['email'])
        self._check_prospect(results['prospect'])

    def test_update(self):
        results = self.pardot.prospects.create_by_email(email=self.email_address, first_name=self.first_name, last_name='McGee')

        prospect = results['prospect']
        self.assertEquals('McGee', prospect['last_name'])

        with self.assertRaises(PardotAPIArgumentError):
            self.pardot.prospects.update_by_email(id=prospect['id'], last_name='Ferdle')

        self.pardot.prospects.update_by_email(email=self.email_address, last_name='Ferdle')

        results = self.pardot.prospects.read_by_id(prospect['id'])
        self.assertEquals('Ferdle', results['prospect']['last_name'])

        with self.assertRaises(PardotAPIArgumentError):
            self.pardot.prospects.update_by_id(email=self.email_address, last_name='Ferdle')

        self.pardot.prospects.update_by_id(id=prospect['id'], last_name='Klampett')

        results = self.pardot.prospects.read_by_id(prospect['id'])
        self.assertEquals('Klampett', results['prospect']['last_name'])

    def test_upsert(self):
        with self.assertRaises(PardotAPIArgumentError):
            results = self.pardot.prospects.upsert_by_email(first_name=self.first_name, last_name=self.last_name)

        results = self.pardot.prospects.upsert_by_email(email=self.email_address, first_name=self.first_name, last_name=self.last_name)

        prospect = results['prospect']
        self._check_prospect(prospect)

        with self.assertRaises(PardotAPIArgumentError):
            self.pardot.prospects.upsert_by_id(email=prospect['id'], last_name='Ferdle')

        self.pardot.prospects.upsert_by_email(email=self.email_address, first_name=self.first_name, last_name='Ferdle')

        results = self.pardot.prospects.read_by_email(prospect['email'])
        self.assertEquals('Ferdle', results['prospect']['last_name'])
        self.assertEquals(prospect['id'], results['prospect']['id'])

    def test_delete(self):
        results = self.pardot.prospects.create_by_email(email=self.email_address, first_name=self.first_name, last_name=self.last_name)
        prospect = results['prospect']

        with self.assertRaises(PardotAPIArgumentError):
            self.pardot.prospects.delete_by_email(id=prospect['id'])

        with self.assertRaises(PardotAPIArgumentError):
            self.pardot.prospects.delete_by_id(email=prospect['email'])

        results = self.pardot.prospects.read_by_id(prospect['id'])
        self.pardot.prospects.delete_by_id(id=prospect['id'])
        with self.assertRaises(PardotAPIError):
            results = self.pardot.prospects.read_by_id(prospect['id'])
