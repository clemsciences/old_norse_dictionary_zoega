"""
Code to analyze dictionary entries
"""

import os
import codecs
# import re
from xml.etree import ElementTree


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
        for filename in self.filenames:
            with codecs.open(os.path.join(self.path, filename), "r", encoding="utf8") as f:
                self.chapters.append(FirstLetterFile(f.read()))
        return self.chapters


class FirstLetterFile:
    """
    Extract entries from a file
    """
    def __init__(self, text):
        self.text = text
        self.entries = []
        self.extract_entries()

    def extract_entries(self):
        entry_texts = []
        i = -1
        for line in self.text.split("\n"):
            if len(line) > 0:
                if line[0] == "\t":
                    if len(entry_texts[i]) > 0:
                        entry_texts[i].append(line)
                    else:
                        print("problem", line)
                else:
                    entry_texts.append([line])
                    i += 1
        for entry_text in entry_texts:
            self.entries.append(Entry(entry_text))


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

    def __init__(self, lines):

        self.lines = lines
        self.word = self.lines[0]
        print(self.word)
        if len(lines) > 1:
            self.description = self.lines[1:]
            for line in self.description:
                print(repr(line))
                line = line.replace("&", "")
                line_tree = ElementTree.fromstring(line)
                # print(line_tree)
                # m = re.search(r"\[m", line)
                # if m is not None:
                #     print(line[m.end()])

            # self.description = [line.strip() for line in self.description]
            # self.description = [re.sub(r"\[m[0-9]*\]", "", line) for line in self.description]
            # self.description = [re.sub(r"\[/m\]", "", line) for line in self.description]
        else:
            self.description = []

    def extract_pos(self):
        pass


if __name__ == "__main__":
    d = DictionaryDSL("entries")
    the_chapters = d.get_first_letter_files()
    print(the_chapters[0].entries[0].lines)
    print(the_chapters[0].entries[0].description)
