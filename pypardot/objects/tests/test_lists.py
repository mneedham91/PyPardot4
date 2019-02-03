import unittest

from pypardot.errors import PardotAPIArgumentError, PardotAPIError
from .test_base import MyBaseTestCase, OBJECT_FIELD_MAP, CONFIG_EXISTS


@unittest.skipUnless(CONFIG_EXISTS, 'Requires Pardot configuration in config.py')
class TestLists(MyBaseTestCase):
	_data = {}

	def setUp(self):
		self._data = self.init_object_data(OBJECT_FIELD_MAP['list'])

		# create a list for testing
		try:
			results = self.pardot.lists.create(**self._data)
			self._data['id'] = results['list']['id']
		except PardotAPIError as e:
			print "could not create list {}: {}".format(e.err_code, e.message)
			raise e

	def tearDown(self):
		try:
			self.pardot.lists.delete(id=self._data['id'])
		except PardotAPIError as e:
			if e.err_code != 4:
				raise e

	def test_list_read(self):
		results = self.pardot.lists.read(id=self._data['id'])
		read_result = results['list']
		self.assertEqual(read_result['name'], self._data['name'])
		self.assertEqual(read_result['title'], self._data['title'])
		self.assertEqual(read_result['description'], self._data['description'])

	def test_list_update(self):
		results = self.pardot.lists.update(
			id=self._data['id'], title='Blah Blah Title',
			description='Blah Blah Description', is_crm_visible=True, is_dynamic=True, is_public=True)
		update_result = results['list']
		self.assertEqual(update_result['title'], 'Blah Blah Title')
		self.assertEqual(update_result['description'], 'Blah Blah Description')
		# Won't update since dynamic boolean is not editable
		self.assertEqual(update_result['is_dynamic'], self._data['is_dynamic'])
		self.assertEqual(update_result['is_public'], True)
		self.assertEqual(update_result['is_crm_visible'], True)

	def test_list_delete(self):
		results = self.pardot.lists.query(name=self._data['name'])
		# Make sure all existing Test Lists are removed
		for result in results['list']:
			# skip test list last created
			if result['id'] == self._data['id']:
				continue
			try:
				delete_res = self.pardot.lists.delete(id=result['id'])
				self.assertEqual(delete_res, 204)
			except PardotAPIError as e:
				if e.err_code != 4:
					raise e
		self.assertTrue(True)
