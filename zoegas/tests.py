"""Test for lemmatizer"""

import unittest
from cltk.corpus import swadesh

from zoegas.reader import Dictionary, dictionary_name


class TestOldNorse(unittest.TestCase):
    def setUp(self):
        self.d = Dictionary(dictionary_name)

    def test_lookup(self):
        word = swadesh.swadesh_old_norse[3]
        print(word)
        entry = self.d.find(word)
        print(entry)

    def test_personnal_preonoun(self):
        word = swadesh.swadesh_old_norse[0]
        print(word)
        entries = self.d.find(word)
        print(entries.description)





