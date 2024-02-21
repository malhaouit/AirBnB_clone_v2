#!/usr/bin/python3
""" """
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os


class test_basemodel(unittest.TestCase):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = 'BaseModel'
        self.value = BaseModel

    def setUp(self):
        """ """
        pass

    def tearDown(self):
        try:
            os.remove('file.json')
        except:
            pass

    def test_default(self):
        """ """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """ """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """ Testing save """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open('file.json', 'r') as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """ """
        i = self.value()
        self.assertEqual(str(i), '[{}] ({}) {}'.format(self.name, i.id,
                         i.__dict__))

    def test_todict(self):
        """ """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_none(self):
        """ """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """ """
        unknown_key = 'unexpected_attribute'
        unknown_value = 'test'
        instance = self.value(**{unknown_key: unknown_value})
        # Check that the unknown attribute is set on the instance
        self.assertTrue(
                hasattr(instance, unknown_key),
                f"Instance should have an attribute '{unknown_key}'.")
        self.assertEqual(
                getattr(instance, unknown_key), unknown_value,
                f"Attribute '{unknown_key}'\
                        should be set to '{unknown_value}'.")

    def test_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime.datetime)

    def test_updated_at(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.updated_at), datetime.datetime)
        n = new.to_dict()
        new = BaseModel(**n)
        self.assertFalse(new.created_at == new.updated_at)

    def test_dynamic_init_with_params(self):
        """Test instantiation with dynamic parameters."""
        name_with_underscores = "Alice_Purry"
        description_with_quotes = 'A \"famous\" cat'
        age = 5
        weight = 9.5
        obj = self.value(
                name=name_with_underscores,
                description=description_with_quotes, age=age, weight=weight)
        self.assertEqual(obj.name, name_with_underscores)
        self.assertEqual(
                obj.description, description_with_quotes.replace('\"', '"'))
        self.assertEqual(obj.age, age)
        self.assertTrue(isinstance(obj.age, int))
        self.assertEqual(obj.weight, weight)
        self.assertTrue(isinstance(obj.weight, float))
