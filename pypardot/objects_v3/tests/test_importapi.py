import csv, os, unittest
from tempfile import NamedTemporaryFile

from pypardot.client import PardotAPI
from pypardot.errors import PardotAPIArgumentError, PardotAPIError

try:
    from pypardot.objects_v3.tests.config import *
    CONFIG_EXISTS = True
except SystemError as e:
    CONFIG_EXISTS = False


@unittest.skipUnless(CONFIG_EXISTS, 'Requires Pardot configuration in config.py')
class TestImportApi(unittest.TestCase):
    def setUp(self, delete=False):
        self.pardot = PardotAPI(email=PARDOT_USER, password=PARDOT_PASSWORD,
                                user_key=PARDOT_USER_KEY, version=3)
        self.pardot.authenticate()

        self.sample_record = {'email': 'parrot@harbles.com',
                              'first_name': 'Pickles',
                              'last_name': 'Zardnif'}

        # Make sure there isn't an existing prospect in the test account.
        if delete:
            try:
                self.pardot.prospects.delete_by_email(email=self.sample_record['email'])
            except PardotAPIError as e:
                # Error code 4 is raised if the prospect doesn't exist.
                if e.err_code != 4:
                    raise e

    def tearDown(self, delete=False):
        if delete:
            try:
                self.pardot.prospects.delete_by_email(email=self.sample_record['email'])
            except PardotAPIError as e:
                # Error code 4 is raised if the prospect doesn't exist.
                if e.err_code != 4:
                    raise e
        os.unlink(self.tempfile.name)
        assert not os.path.exists(self.tempfile.name)
        self.tempfile = None

    def _write_csv(self):
        self.tempfile = NamedTemporaryFile(mode='w', delete=False)
        field_names = self.sample_record.keys()
        writer = csv.DictWriter(self.tempfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerow(self.sample_record)
        self.tempfile.close()
        return self.tempfile.name

    def _print_csv(self):
        print(self.tempfile.name + ':')
        with open(self.tempfile.name) as f:
            print(f.read())

    def test_create_and_read(self):
        file_name = self._write_csv()
        # self._print_csv()
        results = self.pardot.importapi.create(
            operation='Upsert', object='Prospect')
        batch_id = results['id']

        results = self.pardot.importapi.add_batch(id=batch_id,
                                                  file_name=file_name)

        results = self.pardot.importapi.update(id=batch_id, state='Ready')
        assert results['state'] == 'Waiting'

    def test_create(self):
        file_name = self._write_csv()
        # self._print_csv()
        results = self.pardot.importapi.create(
            file_name=file_name, operation='Upsert', object='Prospect')
        batch_id = results['id']
        results = self.pardot.importapi.update(id=batch_id, state='Ready')
        assert results['state'] == 'Waiting'
