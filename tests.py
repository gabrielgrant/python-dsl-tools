#!/usr/bin/env python

import unittest2 as unittest

from dsl_tools import *

class KWArgsAutoSaverTests(unittest.TestCase):
    def test_kwargs_saved(self):
        kwaas = KWArgAutoSaver(my_key='my_val')
        self.assertEqual(kwaas.my_key, 'my_val')

class ClassPropertyTests(unittest.TestCase):
    def test_getter(self):
        class Foo(object):
            @ReadOnlyClassProperty
            def name(cls):
                return cls.__name__
        self.assertEqual(Foo.name, 'Foo')
        self.assertEqual(Foo().name, 'Foo')
    @unittest.skip("setters don't work")
    def test_setter_decorator(self):
        class Foo(object):
            _var = 5
            @ClassProperty
            def var(cls):
                return cls._var
            @var.setter
            def var(cls, val):
                cls._var = val
        self.assertEqual(Foo.var, 5)
        self.assertEqual(Foo._var, 5)
        Foo.var = 6
        self.assertEqual(Foo.var, 6)
        self.assertEqual(Foo._var, 6)
    @unittest.skip("setters don't work")
    def test_setter(self):
        class Foo(object):
            _var = 5
            def _get_var(cls):
                return cls._var
            def _set_var(cls, val):
                cls._var = val
            var = ClassProperty(_get_var, _set_var)
        self.assertEqual(Foo.var, 5)
        self.assertEqual(Foo._var, 5)
        print Foo.__dict__
        Foo.var = 6
        print Foo.__dict__
        self.assertEqual(Foo.var, 6)
        self.assertEqual(Foo._var, 6)


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
