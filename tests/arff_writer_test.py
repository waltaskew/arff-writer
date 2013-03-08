#pylint: disable=R0904
"""Tests for the arff_writer module."""


import datetime
import unittest

import arff_writer


class FeatureFunctionTest(unittest.TestCase):
    """Tests for the FeatureFunction class."""

    def test_attribute_string(self):
        """Test the attribute_string method."""

        feature_func = arff_writer.FeatureFunction(
                lambda x: x,
                attribute_name='snakes',
                attribute_type='numeric')
        self.assertEqual(
                feature_func.attribute_string(),
                '@ATTRIBUTE snakes numeric')

        feature_func = arff_writer.FeatureFunction(
                lambda x: x,
                attribute_name='snakes_moo',
                attribute_type='integer')
        self.assertEqual(
                feature_func.attribute_string(),
                '@ATTRIBUTE snakes_moo integer')

        feature_func = arff_writer.FeatureFunction(
                lambda x: x,
                attribute_name='snakes_hiss',
                attribute_type='real')
        self.assertEqual(
                feature_func.attribute_string(),
                '@ATTRIBUTE snakes_hiss real')

        feature_func = arff_writer.FeatureFunction(
                lambda x: x,
                attribute_name='snakes_sleep',
                attribute_type='nominal',
                nominals=['boo', 'bah', '"beep"'])
        self.assertEqual(
                feature_func.attribute_string(),
                r'@ATTRIBUTE snakes_sleep {"boo","bah","\"beep\""}')

        feature_func = arff_writer.FeatureFunction(
                lambda x: x,
                attribute_name='snakes_explode',
                attribute_type='string')
        self.assertEqual(
                feature_func.attribute_string(),
                '@ATTRIBUTE snakes_explode string')

        feature_func = arff_writer.FeatureFunction(
                lambda x: x,
                attribute_name='snakes_bloop',
                attribute_type='date')
        self.assertEqual(
                feature_func.attribute_string(),
                '@ATTRIBUTE snakes_bloop date')

    def test_set_type_from_val(self):
        """Test the set_type_from_val method."""
        feature_func = arff_writer.FeatureFunction(lambda x: x)

        feature_func.set_type_from_val('a')
        self.assertEqual(feature_func.attribute_type, 'string')

        feature_func.set_type_from_val(1)
        self.assertEqual(feature_func.attribute_type, 'numeric')

        feature_func.set_type_from_val(datetime.datetime(1, 1, 1))
        self.assertEqual(feature_func.attribute_type, 'date')

        feature_func.set_type_from_val(True)
        self.assertEqual(feature_func.attribute_type, 'nominal')
        self.assertEqual(feature_func.nominals, [str(True), str(False)])

    def test_call(self):
        """Test the __call__ method and its type inference magic."""
        feature_func = arff_writer.FeatureFunction(lambda: 1)
        result = feature_func()
        self.assertEqual(result, '1.0')
        self.assertEqual(feature_func.attribute_type, 'numeric')


class ArfWriterTest(unittest.TestCase):
    """Tests for the arff_writer module."""

    def test_feature_decorator(self):
        """Test the feature function's use as a decorator."""
        #pylint: disable=E0102
        #pylint: disable=C0111
        #pylint: disable=C0321
        @arff_writer.feature()
        def test(): pass
        self.assertEqual(test.attribute_name, 'test')

        @arff_writer.feature(fname='moo')
        def test(): pass
        self.assertEqual(test.attribute_name, 'moo')

        @arff_writer.feature(fname='moo', returns='string')
        def test(): pass
        self.assertEqual(test.attribute_name, 'moo')
        self.assertEqual(test.attribute_type, 'string')

        @arff_writer.feature(returns='nominal', nominals=['a', 'b'])
        def test(): pass
        self.assertEqual(test.attribute_name, 'test')
        self.assertEqual(test.attribute_type, 'nominal')
        self.assertEqual(test.nominals, ['a', 'b'])

        with self.assertRaises(ValueError):
            @arff_writer.feature(returns='nominal')
            def test(): pass

    def test_get_header(self):
        """Test the get_header function."""
        funcs = [
                arff_writer.FeatureFunction(
                    lambda: 1,
                    attribute_name='snakes',
                    attribute_type='numeric'),
                arff_writer.FeatureFunction(
                    lambda: 'a',
                    attribute_name='cows',
                    attribute_type='string')
            ]
        self.assertEqual(arff_writer.get_header(
            funcs, 'cake', 'flavor', ['apple', 'cherry']),
"""@RELATION cake


@ATTRIBUTE snakes numeric
@ATTRIBUTE cows string
@ATTRIBUTE flavor {"apple","cherry"}


@DATA""")

    def test_build_feature_file(self):
        """Test the build_feature_file"""

        def fake_module():
            """This will be the make-believe module full of feature
            functions for our tests.
            """
            pass
        fake_module.snakes = arff_writer.FeatureFunction(
                lambda x: 1,
                attribute_name='snakes')
        fake_module.cows = arff_writer.FeatureFunction(
                lambda x: 'a',
                attribute_name='cows')

        self.assertEqual(arff_writer.build_feature_file(
            'cake', fake_module, [('a', 'apple'), ('b', 'banana')], 'flavor'),
'''@RELATION cake


@ATTRIBUTE cows string
@ATTRIBUTE snakes numeric
@ATTRIBUTE flavor {"apple","banana"}


@DATA
"a",1.0,"apple"
"a",1.0,"banana"''')
