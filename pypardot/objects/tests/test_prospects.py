import unittest

from pypardot.errors import PardotAPIArgumentError, PardotAPIError
from .test_base import MyBaseTestCase, CONFIG_EXISTS, OBJECT_FIELD_MAP


@unittest.skipUnless(CONFIG_EXISTS, 'Requires Pardot configuration in config.py')
class TestProspects(MyBaseTestCase):
	_data = {}

	def setUp(self):
		self._data = self.init_object_data(OBJECT_FIELD_MAP['prospect'])
		self._data['email'] = 'parrot@harbles.com'
		self._data['first_name'] = 'Pickles'
		self._data['last_name'] = 'Zardnif'
		self._data['campaign_id'] = 1201

		# create test prospect
		try:
			results = self.pardot.prospects.create(**self._data)
			self._data['id'] = results['prospect']['id']
		except PardotAPIError as e:
			print "could not create prospect {}: {}".format(e.err_code, e.message)
			raise e

	def tearDown(self):
		try:
			self.pardot.prospects.delete_by_id(id=self._data['id'])
		except PardotAPIError as e:
			# Error code 4 is raised if the prospect doesn't exist.
			if e.err_code != 4:
				raise e

	def _check_prospect(self, prosp):
		prosp_arr = prosp if type(prosp) is list else [prosp]
		for p in prosp_arr:
			self.assertEquals(self._data['email'], p['email'])

	# upserts / updates change these values
	# self.assertEquals(self._data['first_name'], p['first_name'])
	# self.assertEquals(self._data['last_name'], p['last_name'])

	def test_prospect_read(self):
		with self.assertRaises(PardotAPIArgumentError):
			self.pardot.prospects.create(
				first_name=self._data['first_name'],
				last_name=self._data['last_name'])
		with self.assertRaises(PardotAPIArgumentError):
			self.pardot.prospects.read_by_id(email='test@test.com')
		with self.assertRaises(PardotAPIArgumentError):
			self.pardot.prospects.read_by_email(id='test')

		results = self.pardot.prospects.read_by_id(id=self._data['id'])
		self._check_prospect(results['prospect'])

		results = self.pardot.prospects.read_by_email(email=self._data['email'])
		self._check_prospect(results['prospect'])

	def test_prospect_update(self):
		with self.assertRaises(PardotAPIArgumentError):
			self.pardot.prospects.update_by_id(email=self._data['email'], last_name='Ferdle')
		with self.assertRaises(PardotAPIError):
			self.pardot.prospects.update_by_id(id=-1, last_name='Ferdle')

		results = self.pardot.prospects.update_by_id(
			id=self._data['id'], last_name='McGee',
			website='http://www.yahoo.com')
		self.assertEquals('McGee', results['prospect']['last_name'])
		self.assertEquals('http://www.yahoo.com', results['prospect']['website'])

	def test_prospect_upsert_delete(self):
		with self.assertRaises(PardotAPIArgumentError):
			self.pardot.prospects.upsert_by_email(first_name=self._data['first_name'])
		with self.assertRaises(PardotAPIArgumentError):
			self.pardot.prospects.upsert_by_id(email=self._data['id'], last_name='Ferdle')

		results = self.pardot.prospects.upsert_by_email(
			id=self._data['id'], email=self._data['email'],
			first_name='Billy')
		self.assertEquals('Billy', results['prospect']['first_name'])

		results = self.pardot.prospects.upsert_by_id(id=self._data['id'], first_name='Bob')
		self.assertEquals('Bob', results['prospect']['first_name'])

		data_copy = self._data.copy()
		data_copy['email'] = 'macaw@harbles.com'
		new_results = self.pardot.prospects.upsert_by_email(email=data_copy['email'], first_name='Johnny')
		self.assertEquals('Johnny', new_results['prospect']['first_name'])
		self.assertEquals('macaw@harbles.com', new_results['prospect']['email'])
		self.assertTrue(self._data['id'] != new_results['prospect']['id'])

		with self.assertRaises(PardotAPIArgumentError):
			self.pardot.prospects.delete_by_id(email=self._data['id'])
		with self.assertRaises(PardotAPIArgumentError):
			self.pardot.prospects.delete_by_fid(id=self._data['id'])

		delete_res = self.pardot.prospects.delete_by_id(id=new_results['prospect']['id'])
		self.assertTrue(delete_res)

	def test_prospect_delete(self):
		results = self.pardot.prospects.query(updated_after='yesterday')
		total = 0
		test_total = 0
		not_test_total = 0

		for result in results['prospect']:
			total = total + 1
			if result['id'] == self._data['id']:
				print "SKIPPING TEST RECORD------"
				continue
			if not result['email'].endswith('@harbles.com'):
				not_test_total = not_test_total + 1
				print('NON-TEST REC ID: {}, Email: {}, Website: {}'.format(
					result['id'], result['email'], result['website']))
			else:
				# ensure all existing prospect test accounts are removed
				test_total = test_total + 1
				print('TEST REC ID: {}, Email: {}, Website: {}'.format(
					result['id'], result['email'], result['website']))
				try:
					delete_res = self.pardot.prospects.delete_by_id(id=result['id'])
					self.assertTrue(delete_res)
				except PardotAPIError as e:
					if e.err_code != 4:
						raise e

		print "nontest {}, test {}, total {}".format(not_test_total, test_total, total)
		self.assertTrue(True)
