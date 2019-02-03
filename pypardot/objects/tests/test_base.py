import unittest

from pypardot.client import PardotAPI
from pypardot.errors import PardotAPIArgumentError, PardotAPIError

try:
	from pypardot.objects.tests.config import *

	CONFIG_EXISTS = True
except SystemError as e:
	CONFIG_EXISTS = False

TEST_STRING_PREFIX = 'PyPardot Test'
TEST_BOOLEAN_VALUE = False

# VALUES WITH * have to be individually tested as they are not generic
# e.g. may have multiple sets of parameters with available operations
# or input parameter set may be different, etc.
SUPPORTED_API_OPERATIONS = {
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
class MyBaseTestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		"""On inherited classes, run our `setUp` method"""
		# Inspired via http://stackoverflow.com/questions/1323455/python-unit-test-with-base-and-sub-class/17696807#17696807
		if cls is not MyBaseTestCase and cls.setUp is not MyBaseTestCase.setUp:
			orig_setUp = cls.setUp

			def setUpOverride(self, *args, **kwargs):
				MyBaseTestCase.setUp(self)
				return orig_setUp(self, *args, **kwargs)

			cls.setUp = setUpOverride

	def setUp(self):
		self.pardot = PardotAPI(email=PARDOT_USER, password=PARDOT_PASSWORD, user_key=PARDOT_USER_KEY)
		self.pardot.authenticate()

	def tearDown(self):
		pass

	def init_object(self, field_map):
		obj = {}
		for k, v in field_map.iteritems():
			if k in set(['id','created_at','updated_at']):
				continue
			else:
				if v['datatype'] == 'string':
					obj[k] = '{} {}'.format(TEST_STRING_PREFIX, k.capitalize())
				elif v['datatype'] == 'boolean':
					obj[k] = TEST_BOOLEAN_VALUE
				else:
					raise Exception('unrecognized datatype {}'.format(v['datatype']))

		return obj