from .mock_util import create_object
from django.test import TestCase


class TestMockUtil(TestCase):

    def test_create_object_1(self):
        attributes = {"id": 12}
        result = create_object(attributes)
        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.id, attributes["id"])

    def test_create_object_2(self):
        attributes = {"id": 12, "name": "I have a name!"}
        result = create_object(attributes)
        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.id, attributes["id"])
        self.assertEqual(result.name, attributes["name"])

    def test_create_object_3(self):
        attributes = {"id": 12, "name": {"first": "Joe", "last": "something"}}
        result = create_object(attributes)
        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.name.first, attributes["name"]["first"])
        self.assertEqual(result.name.last, attributes["name"]["last"])


    def test_create_object_4(self):
        attributes = {"id": 12, "possessions" : ["car", "phone", "keys"]}
        result = create_object(attributes)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "possessions"))
        self.assertEqual(result.id, attributes["id"])
        self.assertEqual(result.possessions, attributes["possessions"])
        self.assertEqual(len(result.possessions), 3)

    def test_create_object_5(self):
        attributes = {"id": 12, "possessions": [{"name": "meme"}, {"name": "lit"}]}
        result = create_object(attributes)
        self.assertTrue(hasattr(result, "id"))
        self.assertTrue(hasattr(result, "possessions"))
        self.assertEqual(result.id, attributes["id"])
        self.assertEqual(len(result.possessions), 2)
        self.assertEqual(result.possessions[0].name, "meme")
        self.assertEqual(result.possessions[1].name, "lit")

