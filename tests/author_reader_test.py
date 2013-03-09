"""Tests for the author_reader module."""


import unittest

import author_reader


class AuthorReaderTest(unittest.TestCase):
    """Tests for the author_reader module."""

    def test_parse_guttenburg(self):
        """Test the parse_guttenburg function."""
        test = """blah blah blah
*** START OF THIS PROJECT GUTENBERG EBOOK THE GIRL WITH THE GOLDEN EYES ***
beautiful words
*** END OF THIS PROJECT GUTENBERG EBOOK THE GIRL WITH THE GOLDEN EYES ***
blah blah blah"""
        self.assertEqual(
                author_reader.parse_guttenburg(test),
                "beautiful words")
