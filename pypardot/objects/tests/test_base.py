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

OBJECT_FIELD_MAP = {
	'list': {
		'id': {'datatype': 'integer', 'required': True, 'editable': False},
		'name': {'datatype': 'string', 'required': False, 'editable': True},
		'is_public': {'datatype': 'boolean', 'required': False, 'editable': True},
		'is_dynamic': {'datatype': 'boolean', 'required': False, 'editable': False},
		'title': {'datatype': 'string', 'required': False, 'editable': True},
		'description': {'datatype': 'string', 'required': False, 'editable': True},
		'is_crm_visible': {'datatype': 'boolean', 'required': False, 'editable': True},
		'created_at': {'datatype': 'timestamp', 'required': False, 'editable': False},
		'updated_at': {'datatype': 'timestamp', 'required': False, 'editable': False},
	},
	'listMembership': {
		'id': {'datatype': 'integer', 'required': True, 'editable': False},
		'list_id': {'datatype': 'integer', 'required': True, 'editable': False, 'fk': 'List'},
		'prospect_id': {'datatype': 'integer', 'required': True, 'editable': False, 'fk': 'Prospect'},
		'opted_out': {'datatype': 'integer', 'required': False, 'editable': True},
		'created_at': {'datatype': 'timestamp', 'required': False, 'editable': False},
		'updated_at': {'datatype': 'timestamp', 'required': False, 'editable': False},
	},
	'prospect': {
		'id': {'datatype': 'integer', 'required': True, 'editable': False},
		'campaign_id': {'datatype': 'integer', 'required': False, 'editable': True, 'fk': 'Campaign'},
		'first_name': {'datatype': 'string', 'required': False, 'editable': True},
		'last_name': {'datatype': 'string', 'required': False, 'editable': True},
		'email': {'datatype': 'string', 'required': True, 'editable': True},
	},
}


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

	def init_object_data(self, field_map):
		data = {}
		for k, v in field_map.iteritems():
			if k in set(['id', 'created_at', 'updated_at']):
				continue
			else:
				if v['datatype'] == 'string':
					data[k] = '{} {}'.format(TEST_STRING_PREFIX, k.capitalize())
				elif v['datatype'] == 'boolean':
					data[k] = TEST_BOOLEAN_VALUE
				elif v['datatype'] == 'integer' and 'fk' in v:
					data[k] = 1
				else:
					raise Exception('unrecognized datatype {}'.format(v['datatype']))

		return data
