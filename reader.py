"""
Code to analyze dictionary entries
"""

import os
import codecs
import re
from xml.etree import ElementTree
from xml.etree.ElementTree import XMLParser

from constants import dheads, postags


def clean(text):
    if text is not None:
        text = re.sub(r"\t", "", text)
        text = re.sub(r"\n", "", text)
        return text
    return text


class Dictionary:
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        self.tree = ElementTree.ElementTree()

    def get_entries(self):
        self.tree.parse(self.filename, XMLParser(encoding='utf-8'))
        for entry in self.tree.iter("entry"):
            self.entries.append(Entry(entry))

    def find(self, word):
        if len(self.entries) == 0:
            self.get_entries()
        if len(word) > 0:
            for entry in self.entries:
                if entry.word == word:
                    return entry


class DictionaryDSL:
    """
    Extracts the dictionary from a list of files where entries are
    """
    def __init__(self, path):
        self.path = path
        self.filenames = os.listdir(path)
        self.entries = []
        self.chapters = []

    def get_first_letter_files(self):
        self.chapters = {}
        for filename in self.filenames:
            with codecs.open(os.path.join(self.path, filename), "r", encoding="utf8") as f:
                self.chapters[dheads[filename]] = FirstLetterFile(f.read())

    def find(self, word):
        if len(self.chapters) == 0:
            self.get_first_letter_files()
        if len(word) > 0:
            for entry in self.chapters[word[0].lower()].entries:
                if entry.word == word:
                    return entry


class FirstLetterFile:
    """
    Extract entries from a file
    """
    def __init__(self, text):
        self.text = text
        self.entries = []
        self.tree = ElementTree.fromstring(self.text)

        for entry in self.tree:
            self.entries.append(Entry(entry))


class Entry:
    """
    Extract features of en entry
    \[m[0-9]*\] -> meaning
    \[i\] ->
    \[trn\] -> translation
    \[p\] -> grammatical features in abbreviations variable
    \[ref\]
    \[b\]
    """

    def __init__(self, entry_xml):
        self.word = entry_xml.get("word")
        self.description = re.sub(r"\t", "", "".join(entry_xml.itertext()))
        self.pos = [postags[pos.text] for pos in entry_xml.iter("p")]
        self.declensions = []
        self.definition = []

    def extract_pos(self):
        pass


if __name__ == "__main__":
    # d = DictionaryDSL("entries")
    # print(d.find("sær").description)
    # print(d.find("sær").pos)
    d = Dictionary("dictionary.xml")
    print(d.find("sær").description)
    print(d.find("sær").pos)
