"""Grab texts and authors from a corpus directory."""


import os


def find_authors(corpus_dir):
    """Given a corpus directory, find the set of authors by looking at
    its sub-directories.
    """
    return [name for name in os.listdir(corpus_dir) if
            os.path.isdir(os.path.join(corpus_dir, name))]


def iter_text(corpus_dir):
    """Return a generator yielding a text and its author for all
    entries in corpus_dir.
    """
    for author in find_authors(corpus_dir):
        author_dir = os.path.join(corpus_dir, author)
        for text in os.listdir(author_dir):
            text_file = os.path.join(author_dir, text)
            with open(text_file, 'r') as text_file:
                yield text_file.read(), author
