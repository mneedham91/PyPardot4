import unittest

from pypardot.errors import PardotAPIArgumentError, PardotAPIError
from .test_base import MyBaseTestCase, SUPPORTED_API_OPERATIONS, CONFIG_EXISTS, pluralize


@unittest.skipUnless(CONFIG_EXISTS, 'Requires Pardot configuration in config.py')
class TestGenericOps(MyBaseTestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_all_query(self):
		method = 'query'
		errors = {}

		for obj_name in sorted(SUPPORTED_API_OPERATIONS.iterkeys()):
			ops = SUPPORTED_API_OPERATIONS[obj_name]
			if method in set(ops):
				print "[{}.{}]...".format(obj_name, method)
				obj = getattr(self.pardot, pluralize(obj_name).lower())
				try:
					results = getattr(obj, method)(id_greater_than='0')
					key_name = obj_name
					if obj_name == 'listMembership':
						key_name = 'list_membership'
					elif obj_name == 'visitorActivity':
						key_name = 'visitor_activity'
					results_length = len(results[key_name])
					total = results['total_results']
					print "[{}.{}] SUCCESS returned {} of {} total results".format(
						obj_name, method, results_length, total)
					self.assertTrue(total >= 0)
				except PardotAPIError as err:
					print "[{}.{}] API_ERROR {}".format(obj_name, method, err.message)
					errors[obj_name] = err.message

		if len(errors.keys()) > 0:
			self.assertTrue(False)
