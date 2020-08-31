import unittest

from pypardot.errors import PardotAPIArgumentError, PardotAPIError
from .test_base import MyBaseTestCase, SUPPORTED_API_OPERATIONS, CONFIG_EXISTS

ABERRANT_PLURAL_MAP = {
	'dynamicContent': 'dynamicContent',
}

VOWELS = set('aeiou')


def pluralize(singular):
	"""Return plural form of given lowercase singular word (English only). Snatched from:
	http://code.activestate.com/recipes/577781-pluralize-word-convert-singular-word-to-its-plural/
	"""
	if not singular:
		return ''
	plural = ABERRANT_PLURAL_MAP.get(singular)
	if plural:
		return plural
	root = singular
	try:
		if singular[-1] == 'y' and singular[-2] not in VOWELS:
			root = singular[:-1]
			suffix = 'ies'
		elif singular[-1] == 's':
			if singular[-2] in VOWELS:
				if singular[-3:] == 'ius':
					root = singular[:-2]
					suffix = 'i'
				else:
					root = singular[:-1]
					suffix = 'ses'
			else:
				suffix = 'es'
		elif singular[-2:] in ('ch', 'sh'):
			suffix = 'es'
		else:
			suffix = 's'
	except IndexError:
		suffix = 's'
	plural = root + suffix
	return plural


@unittest.skipUnless(CONFIG_EXISTS, 'Requires Pardot configuration in config.py')
class TestGenericOps(MyBaseTestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_all_query(self):
		method = 'query'
		errors = {}

		for obj_name in sorted(SUPPORTED_API_OPERATIONS.keys()):
			ops = SUPPORTED_API_OPERATIONS[obj_name]
			if method in set(ops):
				print("[{}.{}]...".format(obj_name, method))
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
					print("[{}.{}] SUCCESS returned {} of {} total results".format(
						obj_name, method, results_length, total))
					self.assertTrue(total >= 0)
				except PardotAPIError as err:
					print("[{}.{}] API_ERROR {}".format(obj_name, method, err.message))
					errors[obj_name] = err.message

		if len(list(errors.keys())) > 0:
			self.assertTrue(False)
