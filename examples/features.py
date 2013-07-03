"""Example of a feature function file."""


from __future__ import division

import arff_writer


@arff_writer.feature()
def word_count(text):
    """Total number of words in the text."""
    return len(text.split())


@arff_writer.feature()
def lexical_diversity(text):
    """Total number of words in the text divided by the number of
    distinct words in the text.
    """
    words = [word.lower() for word in text.split()]
    distinct_words = set(words)
    return len(distinct_words) / len(words)
