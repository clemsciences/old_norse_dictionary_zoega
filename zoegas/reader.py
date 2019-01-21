"""
Code to analyze Zoëga's dictionary entries
"""

import re
from typing import Optional

from xml.etree import ElementTree
from xml.etree.ElementTree import XMLParser

from cltk.phonology import utils as phu
from cltk.phonology.old_norse import transcription as ont
from cltk.phonology.syllabify import Syllabifier
from cltk.tokenize.word import tokenize_old_norse_words
from cltk.corpus.old_norse.syllabifier import hierarchy, invalid_onsets
from cltk.text_reuse.levenshtein import Levenshtein

from zoegas.constants import postags, dictionary_name

# phonetic transcriber
phonetic_transcriber = phu.Transcriber(ont.DIPHTHONGS_IPA, ont.DIPHTHONGS_IPA_class, ont.IPA_class, ont.old_norse_rules)

# Old Norse syllabifier
s = Syllabifier(language="old_norse", break_geminants=True)
s.set_invalid_onsets(invalid_onsets)
s.set_hierarchy(hierarchy)


def clean(text: str) -> Optional[str]:
    """

    :param text:
    :return:
    """
    if text is not None:
        text = re.sub(r"\t", "", text)
        text = re.sub(r"\n", "", text)
        return text
    else:
        return None


def is_pure_word(text: str) -> bool:
    """
    Words containing parentheses, whitespaces, hyphens and w characters are not considered as proper words
    :param text:
    :return:
    """
    return "-" not in text and "(" not in text and ")" not in text and " " not in text and "w" not in text


class Entry:
    """
    Extract features of en entry
    \[m[0-9]*\] -> meaning
    \[i\] ->
    \[trn\] -> translation
    \[p\] -> grammatical features in abbreviations variable
    \[ref\]
    \[b\]


    >>> d = Dictionary(dictionary_name)
    >>> entry = d.find("skapa")
    >>> entry.word
    'skapa'
    >>> entry.description
    '\\n\\n(að; pret. also skóp), v.\\n\\n1) to shape, form, mould, make (ór Ymis holdi var jörð sköpuð); to create (guð, er mik skóp); s. skegg, to trim the beard; s. skeið, to take a run (þetta dýr ~ði skeið at oss); s. ok skera e-t, or um e-t, to decide, settle (ek skal einn skera ok s. okkar á milli);\\n\\n2) to assign as one’s fate or destiny (ek ~ honum þat, at hann skal eigi lifa lengr en kerti þat brenner); s. e-m aldr, to fashion one’s future life; syni þínum verðr-a sæla sköpuð, bliss is not fated to thy son;\\n\\n3) to fix, appoint (haf þá eina fémuni, er ek ~ þér); s. e-m víti, to impose a fine or penalty; at sköpuðu, in the order of nature, according to the course of nature (væri þat at sköpuðu fyrir aldrs sakir, at þú lifðir lengr okkar); láta skeika at sköpuðu, to let things go their own course (according to fate); láta ~t skera, to let fate decide;\\n\\n4) refl., ~st, to take shape; freista, hvé þá skapist, try how things will go then; Ámundi kvað jarl úáhlýðinn ok mun lítt at s., A. said the earl was self-willed, and little will come of it.\\n\\n'
    >>> entry.pos
    ['s', 'eitthvert', 'eitthvert', 'einhverjum', 'einhverjum', 'reflexive']
    >>> entry.declensions
    []
    >>> entry.definition
    []
    >>> entry.phonetic_transcription
    '[skapa]'
    >>> entry.syllabified_word
    ['skap', 'a']

    """

    def __init__(self, entry_xml):
        self.word = entry_xml.get("word")
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
        """
        # TODO Guess POS of words. It may be extracted from entries.
        :return:
        """
        pass

    def levenshtein_distance(self, other_word: str) -> int:
        """
        Basic use of Levenshtein distance function
        :param other_word:
        :return:
        """
        return Levenshtein.Levenshtein_Distance(self.word, other_word)


class Dictionary:
    """

    """

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

    def find(self, word: str) -> Optional[list]:
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

    def find_approximately(self, word: str, distance_threshold: int = 3) -> list:
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

    def find_beginning_with(self, word: str):
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
                if entry.word is not None and len(entry.word) >= word_length:
                    if entry.word[:word_length] == word:
                        entries.append(entry)
        return entries


if __name__ == "__main__":
    # d = DictionaryDSL("entries")
    # print(d.find("sær").description)
    # print(d.find("sær").pos)
    d = Dictionary(dictionary_name)
    # print(d.find("sær").description)
    # print(d.find("sær").pos)
    # print(d.find("sær").phonetic_transcription)
    # print(d.find("sær").syllabified_word)

    d.find_approximately("lævi", 3)
    for word in ["lævi", "blandit", "eða", "ætt", "jötuns", "Óðs", "mey", "gefna"]:
        found_word = d.find_approximately(word, 3)

        for w in found_word:
            print(w.word)
            print(w.description)
        # print([found_word)
        # print(found_word.description)
