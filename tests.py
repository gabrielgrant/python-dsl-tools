#!/usr/bin/env python

import unittest

from dsl_tools import *

class KWArgsAutoSaverTests(unittest.TestCase):
    def test_kwargs_saved(self):
        kwaas = KWArgAutoSaver(my_key='my_val')
        self.assertEqual(kwaas.my_key, 'my_val')

class DeclarativeMetaclassTests(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    def test_registration(self):
        class Column(object):
            def __init__(self, default_value=None):
                self.default_value = default_value
            def set_name(self, name):
                self.name = name

        def callback(declaration, name):
            declaration.name = name

        class Table(object):
            __metaclass__ = make_declarative_metaclass(
                declared_type=Column,
                declarations_name='columns',
                set_declaration_name_callback=callback
            )
        
        class PersonTable(Table):
            fname = Column(default_value='')
            lname = Column(default_value='')
            gender = Column()
        self.assertEqual(PersonTable.columns['fname'].name, 'fname')
    #def test_filter_func(self):
    #def test_subclassing(self):
    #def test_callback(self):

def main():
    unittest.main()

if __name__ == '__main__':
    main()
