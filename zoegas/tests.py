"""Test for lemmatizer"""

import unittest

from zoegas.reader import Dictionary, dictionary_name


class TestOldNorse(unittest.TestCase):
    def setUp(self):
        self.d = Dictionary(dictionary_name)

    def test_lookup(self):
        word = 'hann'
        print(word)
        entry = self.d.find(word)
        print(entry)

    def test_personnal_preonoun(self):
        word = "ek"
        print(word)
        entries = self.d.find(word)
        print(entries.description)
