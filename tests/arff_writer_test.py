"""Tests for the arff_writer module."""


import datetime
import unittest

import arff_writer


class FeatureFunctionTest(unittest.TestCase):
    """Tests for the arff_writer module."""

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

        feature_func.set_type_from_val(datetime.datetime(1,1,1))
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
