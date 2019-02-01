import unittest

from pypardot.client import PardotAPI
from pypardot.errors import PardotAPIArgumentError, PardotAPIError

try:
	from pypardot.objects.tests.config import *

	CONFIG_EXISTS = True
except SystemError as e:
	CONFIG_EXISTS = False

# VALUES WITH * have to be individually tested as they are not generic
# e.g. may have multiple sets of parameters with available operations
# or input parameter set may be different, etc.

API_SUPPORTED_OPERATIONS = {
	'account': ['read'],
	'campaign': ['query', 'read', 'update', 'create'],
	'customField': ['query', 'read', 'update', 'create', 'delete'],
	'customRedirect': ['query', 'read'],
	'dynamicContent': ['query', 'read'],
	'email': ['read', 'stats'],
	'emailClick': ['query'],
	'emailTemplate': ['read', 'listOneToOne'],
	'form': ['query', 'read'],
	'lifecycleHistory': ['query', 'read'],
	'lifecycleStage': ['query'],
	'list': ['query', 'read', 'update', 'create', 'delete'],
	'listMembership': ['query', 'read*', 'create', 'update*', 'delete'],
	'opportunity': ['query', 'create*', 'read', 'update', 'delete', 'undelete'],
	'prospect': [
		'query', 'assign*', 'unassign*', 'create', 'batchCreate', 'read*', 'update*', 'batchUpdate', 'upsert',
		'batchUpsert', 'delete*'],
	'prospectAccount': ['query', 'create', 'describe', 'read', 'update', 'assign'],
	'tag': ['query', 'read'],
	'tagObject': ['query', 'read'],
	'user': ['query', 'read*'],
	'visitor': ['query', 'assign', 'read'],
	'visitorActivity': ['query', 'read'],
	'visit': ['query*', 'read']
}

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
class TestGenericApiOperations(unittest.TestCase):
	def setUp(self):
		self.pardot = PardotAPI(email=PARDOT_USER, password=PARDOT_PASSWORD, user_key=PARDOT_USER_KEY)
		self.pardot.authenticate()

	def tearDown(self):
		pass

	def test_query(self):
		method = 'query'
		errors = {}

		for obj_name in sorted(API_SUPPORTED_OPERATIONS.iterkeys()):
			ops = API_SUPPORTED_OPERATIONS[obj_name]
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
