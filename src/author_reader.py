"""Grab texts and authors from a corpus directory."""


import os
import re


GUTENBERG_HEADER_RE = re.compile(
        r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK [^\r\n]* \*\*\*")
GUTENBERG_FOOTER_RE = re.compile(
        r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK [^\r\n]* \*\*\*")


def find_authors(corpus_dir):
    """Given a corpus directory, find the set of authors by looking at
    its sub-directories.
    """
    return [name for name in os.listdir(corpus_dir) if
            os.path.isdir(os.path.join(corpus_dir, name))]


def parse_guttenburg(text):
    """Remove starting and trailing guttenburg headers and footers if
    they are present.
    """
    header_match = GUTENBERG_HEADER_RE.search(text)
    if header_match is not None:
        text = text[header_match.end(0):]

    footer_match = GUTENBERG_FOOTER_RE.search(text)
    if footer_match is not None:
        text = text[:footer_match.start(0)]

    return text.strip()


def iter_text(corpus_dir):
    """Return a generator yielding a text and its author for all
    entries in corpus_dir.
    """
    for author in find_authors(corpus_dir):
        author_dir = os.path.join(corpus_dir, author)
        for text_name in os.listdir(author_dir):
            text_file = os.path.join(author_dir, text_name)
            with open(text_file, 'rU') as text_file:
                text = text_file.read()
                yield parse_guttenburg(text), author
