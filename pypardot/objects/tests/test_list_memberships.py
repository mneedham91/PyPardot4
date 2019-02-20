import unittest

from pprint import pprint
from pypardot.errors import PardotAPIArgumentError, PardotAPIError
from .test_base import MyBaseTestCase, CONFIG_EXISTS, OBJECT_FIELD_MAP


@unittest.skipUnless(CONFIG_EXISTS, 'Requires Pardot configuration in config.py')
class TestListMemberships(MyBaseTestCase):
	_data = {}
	_list_data = {}
	_prospect_data = {}
	_membership_data = {}

	def setUp(self):
		self._list_data = self.init_object_data(OBJECT_FIELD_MAP['list'])
		self._list_data['name'] = 'PyPardot Test List Membership Name'
		self._list_data['title'] = 'PyPardot Test List Membership Title'
		self._list_data['description'] = 'PyPardot Test List Membership Description'

		# create a list for testing
		try:
			results = self.pardot.lists.create(**self._list_data)
			self._list_data['id'] = results['list']['id']
		except PardotAPIError as e:
			print "could not create list {}: {}".format(e.err_code, e.message)
			raise e

		self._create_list_membership()

	def tearDown(self):
		try:
			self.pardot.lists.delete(id=self._list_data['id'])
		except PardotAPIError as e:
			if e.err_code != 4:
				raise e

	def _create_list_membership(self):
		# create a random batch of prospects
		try:
			results = self.pardot.prospects.query(last_activity_never=True, score_less_than=0, limit=5)
			for result in results['prospect']:
				self._prospect_data[result['id']] = result
		except PardotAPIError as e:
			print "could not query prospects {}: {}".format(e.err_code, e.message)
			raise e

		for pid in self._prospect_data.iterkeys():
			try:
				result = self.pardot.listmemberships.create(list_id=self._list_data['id'], prospect_id=pid)
				result_lm = result['list_membership']
				self.assertEquals(result_lm['prospect_id'], pid)
				self.assertEquals(result_lm['list_id'], self._list_data['id'])
				self._membership_data[result_lm['id']] = result_lm
			except PardotAPIError as e:
				print "could not create list membership {}: {}".format(e.err_code, e.message)
				raise e

	def test_list_membership_read(self):
		count = 0
		membership_id = self._membership_data.iterkeys().next()
		try:
			results = self.pardot.listmemberships.read_by_id(id=membership_id)
			self.assertEqual(
				results['list_membership']['prospect_id'], self._membership_data[membership_id]['prospect_id'])
			self.assertEqual(results['list_membership']['list_id'], self._membership_data[membership_id]['list_id'])
		except PardotAPIError as e:
			print "could not read list membership {}: {}".format(e.err_code, e.message)
			raise e

		for pid in self._prospect_data.iterkeys():
			try:
				results = self.pardot.listmemberships.read(list_id=self._list_data['id'], prospect_id=pid)
				self.assertTrue(results['list_membership']['id'] > 0)
				count = count + 1
			except PardotAPIError as e:
				print "could not read list membership {}: {}".format(e.err_code, e.message)
				raise e
		self.assertEquals(count, len(self._prospect_data))

	def test_list_membership_update(self):
		count = 0
		for k, v in self._membership_data.iteritems():
			if count % 2 == 0:
				try:
					results = self.pardot.listmemberships.update(
						list_id=v['list_id'], prospect_id=v['prospect_id'], opted_out=True)
					self.assertEquals(results['list_membership']['opted_out'], True)
				except PardotAPIError as e:
					print "could not update list membership by pid/lid {}: {}".format(e.err_code, e.message)
					raise e
			else:
				try:
					results = self.pardot.listmemberships.update_by_id(id=k, opted_out=True)
					self.assertEquals(results['list_membership']['opted_out'], True)
				except PardotAPIError as e:
					print "could not update list membership by id {}: {}".format(e.err_code, e.message)
					raise e

	def test_list_membership_query(self):
		try:
			results = self.pardot.listmemberships.query(deleted=True)
			pprint(results['list_membership'])
			deleted_count = len(results['list_membership'])
			print 'num items: {}'.format(deleted_count)
			self.assertTrue(deleted_count >= 0)
		except PardotAPIError as e:
			print "could not query list membership {}: {}".format(e.err_code, e.message)
			raise e

	def test_list_membership_delete(self):
		member_id1 = self._membership_data.iterkeys().next()
		member_val1 = self._membership_data.pop(member_id1)

		member_id2 = self._membership_data.iterkeys().next()
		member_val2 = self._membership_data.pop(member_id2)

		pprint(member_val1)
		pprint(member_val2)

		try:
			delete_res1 = self.pardot.listmemberships.delete(
				list_id=self._list_data['id'], prospect_id=member_val1['prospect_id'])
			self.assertTrue(delete_res1)
		except PardotAPIError as e:
			print "could not delete list membership {}: {}".format(e.err_code, e.message)
			raise e

		# delete second item by id
		try:
			delete_res2 = self.pardot.listmemberships.delete_by_id(id=member_id2)
			self.assertTrue(delete_res2)
		except PardotAPIError as e:
			print "could not delete list membership {}: {}".format(e.err_code, e.message)
			raise e
