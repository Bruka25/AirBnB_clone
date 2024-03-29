#!/usr/bin/python3
"""Unittest for baseModel class"""

import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_initialization(unittest.TestCase):
    """Class for Unittesting  for initialization of the
       BaseModel class
    """

    def test_no_args_(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_two_models_unique_ids(self):
        base1 = BaseModel()
        base2 = BaseModel()
        self.assertNotEqual(base1.id, base2.id)

    def test_two_models_diff_created_at(self):
        base1 = BaseModel()
        sleep(0.05)
        base2 = BaseModel()
        self.assertLess(base1.created_at, base2.created_at)

    def test_two_models_diffe_updated_at(self):
        base1 = BaseModel()
        sleep(0.05)
        base2 = BaseModel()
        self.assertLess(base1.updated_at, base2.updated_at)

    def test_str_representation(self):
        date = datetime.today()
        date_repr = repr(date)
        base = BaseModel()
        base.id = "123456"
        base.created_at = base.updated_at = date
        basestr = base.__str__()
        self.assertIn("[BaseModel] (123456)", basestr)
        self.assertIn("'id': '123456'", basestr)
        self.assertIn("'created_at': " + date_repr, basestr)
        self.assertIn("'updated_at': " + date_repr, basestr)

    def test_args_unused(self):
        base = BaseModel(None)
        self.assertNotIn(None, base.__dict__.values())

    def test_initialization_with_kwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        base = BaseModel(id="345", created_at=date_iso, updated_at=date_iso)
        self.assertEqual(base.id, "345")
        self.assertEqual(base.created_at, date)
        self.assertEqual(base.updated_at, date)

    def test_initialization_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_initialization_with_args_and_kwargs(self):
        date = datetime.today()
        date_iso = date.isoformat()
        base = BaseModel("12", id="345",
                         created_at=date_iso, updated_at=date_iso)
        self.assertEqual(base.id, "345")
        self.assertEqual(base.created_at, date)
        self.assertEqual(base.updated_at, date)


class TestBaseModel_to_dict(unittest.TestCase):
    """Class for unittesting for testing to_dict
       method of the BaseModel class
    """

    def test_to_type_of_dict(self):
        base = BaseModel()
        self.assertTrue(dict, type(base.to_dict()))

    def test_to_dict_with_correct_keys(self):
        base = BaseModel()
        self.assertIn("id", base.to_dict())
        self.assertIn("created_at", base.to_dict())
        self.assertIn("updated_at", base.to_dict())
        self.assertIn("__class__", base.to_dict())

    def test_to_dict_contains_added_attributes(self):
        base = BaseModel()
        base.name = "Holberton"
        base.my_number = 98
        self.assertIn("name", base.to_dict())
        self.assertIn("my_number", base.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        base = BaseModel()
        base_dict = base.to_dict()
        self.assertEqual(str, type(base_dict["created_at"]))
        self.assertEqual(str, type(base_dict["updated_at"]))

    def test_to_dict_output(self):
        date = datetime.today()
        base = BaseModel()
        base.id = "123456"
        base.created_at = base.updated_at = date
        tdict = {
            'id': '123456',
            '__class__': 'BaseModel',
            'created_at': date.isoformat(),
            'updated_at': date.isoformat()
        }
        self.assertDictEqual(base.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        base = BaseModel()
        self.assertNotEqual(base.to_dict(), base.__dict__)

    def test_to_dict_with_arg(self):
        base = BaseModel()
        with self.assertRaises(TypeError):
            base.to_dict(None)


class TestBaseModel_saving(unittest.TestCase):
    """Class for unittests for testing save method
       of the BaseModel class
    """

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        base = BaseModel()
        sleep(0.05)
        first_updated_at = base.updated_at
        base.save()
        self.assertLess(first_updated_at, base.updated_at)

    def test_two_saves(self):
        base = BaseModel()
        sleep(0.05)
        first_updated_at = base.updated_at
        base.save()
        second_updated_at = base.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        base.save()
        self.assertLess(second_updated_at, base.updated_at)

    def test_save_with_arg(self):
        base = BaseModel()
        with self.assertRaises(TypeError):
            base.save(None)

    def test_save_updates_file(self):
        base = BaseModel()
        base.save()
        baseid = "BaseModel." + base.id
        with open("bruka.json", "r") as f:
            self.assertIn(baseid, f.read())


if __name__ == "__main__":
    unittest.main()
