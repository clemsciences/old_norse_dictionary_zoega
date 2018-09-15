"""
How xml files are built
"""

import os
import codecs
import re
from xml.etree import ElementTree

from constants import heads


def clean(text):
    if text is not None:
        text = re.sub(r"\t", "", text)
        text = re.sub(r"\n", "", text)
        return text
    return text


def transform():
    for filename in os.listdir("entries"):
        with codecs.open(os.path.join("entries", filename), "r", encoding="utf8") as f:
            text = f.read()
        text = text.replace("[", "<")
        text = text.replace("]", ">")
        with codecs.open(os.path.join("entries", filename), "w", encoding="utf8") as f:
            f.write(text)


def transform_mi():
    for filename in os.listdir("entries"):
        with codecs.open(os.path.join("entries", filename), "r", encoding="utf8") as f:
            text = f.readlines()
        lines = []
        for line in text:
            for i in range(1, 6):
                if "<m"+str(i)+">" in line:
                    line_length = len(line)
                    line = line[:line_length-6]
                    line += "</m"+str(i)+">"

            lines.append(line)
        text = os.linesep.join(lines)
        with codecs.open(os.path.join("entries", filename), "w", encoding="utf8") as f:
            f.write(text)


def give_word_tag():
    for filename in os.listdir("entries"):
        with codecs.open(os.path.join("entries", filename), "r", encoding="utf8") as f:
            text = f.readlines()
        lines = []
        for line in text:

            if len(line) > 0:
                if line[0] == "\t":
                    line = line.rstrip()
                else:
                    line = "</word>\n<word>\n"+line.rstrip()
                lines.append(line)
        text = "\n".join(lines)+"\n</word>"
        text = "\n".join(text.split("\n")[1:])
        with codecs.open(os.path.join("entries", filename), "w", encoding="utf8") as f:
            f.write(text)


def remove_double_tab():
    for filename in os.listdir("entries"):
        with codecs.open(os.path.join("entries", filename), "r", encoding="utf8") as f:
            text = f.read().split("\n")
        lines = []
        for line in text:
            print(repr(line))
            if len(line.rstrip()) > 0:
                if line[0] == "\t":
                    line = line.rstrip()[1:]
                lines.append(line)
        text = "\n".join(lines)
        print(repr(text[:20]))
        with codecs.open(os.path.join("entries", filename), "w", encoding="utf8") as f:
            f.write(text)


def change_name_mark():
    for filename in os.listdir("entries"):
        with codecs.open(os.path.join("entries", filename), "r", encoding="utf8") as f:
            text = f.read()
            text = text.replace("<word>", "<entry>")
            text = text.replace("</word>", "</entry>")
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            if len(line) > 0:
                if line[0] in heads:
                    new_lines.append("\t<word>\n\t\t"+line+"\n\t</word>")
                else:
                    new_lines.append(line)
        new_text = "\n".join(new_lines)+"\n</word>"
        with codecs.open(os.path.join("entries", filename), "w", encoding="utf8") as f:
            f.write(new_text)


def add_chapters():
    for filename in os.listdir("entries"):
        with codecs.open(os.path.join("entries", filename), "r", encoding="utf8") as f:
            text = f.read()
        new_text = "<chapter>\n"+text+"\n</chapter>\n"
        with codecs.open(os.path.join("entries", filename), "w", encoding="utf8") as f:
            f.write(new_text)


def replace_strange_characters():
    for filename in os.listdir("entries"):
        with codecs.open(os.path.join("entries", filename), "r", encoding="utf8") as f:
            text = f.read()
            new_text = text.replace("&c.", "")
        with codecs.open(os.path.join("entries", filename), "w", encoding="utf8") as f:
            f.write(new_text)


def add_word_tag():
    for filename in os.listdir("entries"):
        print(filename)
        tree = ElementTree.ElementTree()
        tree.parse(os.path.join("entries", filename))
        for entry in tree.iter("entry"):
            for line in entry:
                if line.tag == "word":
                    word = clean("".join(line.itertext()))
                    entry.set("word", word)
                    entry.remove(line)

        tree.write(os.path.join("entries", filename), encoding="utf8")


if __name__ == "__main__":
    # transform()
    # transform_mi()
    # give_word_tag()
    # remove_double_tab()
    # change_name_mark()
    # add_chapters()
    # replace_strange_characters()
    add_word_tag()
