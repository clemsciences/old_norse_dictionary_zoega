"""
Code to analyze dictionary entries
"""

import re

from xml.etree import ElementTree
from xml.etree.ElementTree import XMLParser

from cltk.phonology import utils as phu
from cltk.phonology.old_norse import transcription as ont
from cltk.phonology.syllabify import Syllabifier
from cltk.tokenize.word import tokenize_old_norse_words
from cltk.corpus.old_norse.syllabifier import hierarchy, invalid_onsets
from cltk.text_reuse.levenshtein import Levenshtein

from constants import postags, dictionary_name

# phonetic transcriber
phonetic_transcriber = phu.Transcriber(ont.DIPHTHONGS_IPA, ont.DIPHTHONGS_IPA_class, ont.IPA_class, ont.old_norse_rules)

# Old Norse syllabifier
s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)
s.set_hierarchy(hierarchy)


def clean(text):
    """

    :param text:
    :return:
    """
    if text is not None:
        text = re.sub(r"\t", "", text)
        text = re.sub(r"\n", "", text)
        return text
    return text


def is_pure_word(text):
    """
    Words containing parentheses, whitespaces, hyphens and w characters are not considered as proper words
    :param text:
    :return:
    """
    return "-" not in text and "(" not in text and ")" not in text and " " not in text and "w" not in text


class Dictionary:
    def __init__(self, filename):
        self.filename = filename
        self.entries = []
        self.tree = ElementTree.ElementTree()

    def get_entries(self):
        """
        Load entries
        :return:
        """
        self.tree.parse(self.filename, XMLParser(encoding='utf-8'))
        for entry in self.tree.iter("entry"):
            self.entries.append(Entry(entry))

    def find(self, word):
        """
        Search a specific word
        :param word:
        :return: Entry instance or None
        """
        if len(self.entries) == 0:
            self.get_entries()
        if len(word) > 0:
            for entry in self.entries:
                if entry.word == word:
                    return entry
        return None

    def find_approximately(self, word, distance_threshold=3):
        """
        Search words which are at most *distance_threshold* distant of *word* argument
        :param word: 
        :param distance_threshold: 
        :return: list of Entry instances
        """""
        entries = []
        if len(self.entries) == 0:
            self.get_entries()
        if len(word) > 0:
            for entry in self.entries:
                if entry.word is not None and is_pure_word(entry.word):
                    if entry.levenshtein_distance(word) < distance_threshold:
                        entries.append(entry)
        return entries

    def find_beginning_with(self, word):
        """
        Find words which start with *word*
        :param word:
        :return: list of Entry instances
        """
        entries = []
        word_length = len(word)
        if len(self.entries) == 0:
            self.get_entries()
        if len(word) > 0:
            for entry in self.entries:
                if len(entry.word) >= word_length:
                    if entry.word[:word_length] == entry.word:
                        entries.append(entry)
        return entries


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
        print(repr(self.word))
        self.description = re.sub(r"\t", "", "".join(entry_xml.itertext()))
        self.pos = [postags[pos.text] for pos in entry_xml.iter("p")]
        self.declensions = []
        self.definition = []
        # if not isinstance(self.word, str):
        #     print(repr(self.word))
        if self.word is None:
            self.phonetic_transcription = ""
            self.syllabified_word = ""
        else:
            self.phonetic_transcription = " ".join([phonetic_transcriber.main(word)
                                                    if word is not None and is_pure_word(word) else ""
                                                    for word in tokenize_old_norse_words(self.word)])
            self.syllabified_word = []
            for word in tokenize_old_norse_words(self.word):
                if word is not None and is_pure_word(word):
                    self.syllabified_word.extend(s.syllabify_SSP(word.lower()))

    def extract_pos(self):
        pass

    def levenshtein_distance(self, other_word):
        return Levenshtein.Levenshtein_Distance(self.word, other_word)


if __name__ == "__main__":
    # d = DictionaryDSL("entries")
    # print(d.find("sær").description)
    # print(d.find("sær").pos)
    d = Dictionary(dictionary_name)
    print(d.find("sær").description)
    print(d.find("sær").pos)
    print(d.find("sær").phonetic_transcription)
    print(d.find("sær").syllabified_word)
