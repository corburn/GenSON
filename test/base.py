import unittest
import jsonschema
from genson import SchemaNode, SchemaRoot


class SchemaTestCase(unittest.TestCase):

    def setUp(self):
        self._schema = self.CLASS()
        self._objects = []
        self._schemas = []

    def set_schema_options(self, **options):
        self._schema = SchemaNode(**options)

    def add_object(self, obj):
        self._schema.add_object(obj)
        self._objects.append(obj)

    def add_schema(self, schema):
        self._schema.add_schema(schema)
        self._schemas.append(schema)

    def assertObjectValidates(self, obj):
        jsonschema.Draft4Validator(self._schema.to_schema()).validate(obj)

    def assertObjectDoesNotValidate(self, obj):
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.Draft4Validator(self._schema.to_schema()).validate(obj)

    def assertResult(self, expected):
        self.assertEqual(self._schema.to_schema(), expected)
        self.assertUserContract()

    def assertUserContract(self):
        self._assertSchemaIsValid()
        self._assertComponentObjectsValidate()

    def _assertSchemaIsValid(self):
        jsonschema.Draft4Validator.check_schema(self._schema.to_schema())

    def _assertComponentObjectsValidate(self):
        compiled_schema = self._schema.to_schema()
        for obj in self._objects:
            jsonschema.Draft4Validator(compiled_schema).validate(obj)


class SchemaNodeTestCase(SchemaTestCase):
    CLASS = SchemaNode


class SchemaRootTestCase(SchemaTestCase):
    CLASS = SchemaRoot


# Python 2 compatibility

if not hasattr(SchemaTestCase, 'assertWarns'):
    import warnings
    from contextlib import contextmanager

    @contextmanager
    def _assertWarns(self, warning):
        """
        Python 2.7 unittest has no assertWarns, so this is a no-op
        dummy method that will allow the tests to pass.
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            yield

    SchemaTestCase.assertWarns = _assertWarns
