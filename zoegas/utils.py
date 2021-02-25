"""
How xml files are built
"""

import codecs
from lxml import etree
import os
import re

# from xml.etree import ElementTree
# from xml.etree.ElementTree import XMLParser
import yaml
# from lxml import etree
from bs4 import BeautifulSoup

from zoegas.constants import real_heads


def clean(text):
    if text is not None:
        text = re.sub(r"\t", "", text)
        text = re.sub(r"\n", "", text)
        return text
    return text


def transform(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for filename in os.listdir(src):
        with codecs.open(os.path.join(src, filename), "r", encoding="utf8") as f:
            text = f.read()
        text = text.replace("[", "<")
        text = text.replace("]", ">")
        text = text.replace("\r", "")
        with codecs.open(os.path.join(dst, filename), "w", encoding="utf8") as f:
            f.write(text)


def transform_mi(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for filename in os.listdir(src):
        with codecs.open(os.path.join(src, filename), "r", encoding="utf8") as f:
            text = f.read().split("\n")
        lines = []
        for line in text:
            for i in range(1, 6):
                if "<m"+str(i)+">" in line:
                    line_length = len(line)
                    j = line[::-1].find("<")
                    line = line[:line_length-j-1]
                    line += "</m"+str(i)+">"

            lines.append(line)
        text = "\n".join(lines)+"\n"

        with codecs.open(os.path.join(dst, filename), "w", encoding="utf8") as f:
            f.write(text)
    print(repr(os.linesep))


def give_word_tag(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for filename in os.listdir(src):
        with codecs.open(os.path.join(src, filename), "r", encoding="utf8") as f:
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
        with codecs.open(os.path.join(dst, filename), "w", encoding="utf8") as f:
            f.write(text)


def remove_double_tab(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for filename in os.listdir(src):
        with codecs.open(os.path.join(src, filename), "r", encoding="utf8") as f:
            text = f.read().split("\n")
        lines = []
        for line in text:
            if len(line.rstrip()) > 0:
                if line[0] == "\t":
                    line = line.rstrip()[1:]
                lines.append(line)
        text = "\n".join(lines)

        with codecs.open(os.path.join(dst, filename), "w", encoding="utf8") as f:
            f.write(text)


def change_name_mark(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for filename in os.listdir(src):
        with codecs.open(os.path.join(src, filename), "r", encoding="utf8") as f:
            text = f.read()
            text = text.replace("<word>", "<entry>")
            text = text.replace("</word>", "</entry>")
            text = text.replace("\r", "")
        lines = text.split("\n")
        new_lines = []
        for line in lines:
            if len(line) > 0:
                if line[0] in real_heads:
                    new_lines.append("\t<word>\n\t\t"+line+"\n\t</word>")
                else:
                    new_lines.append(line)
        new_text = "\n".join(new_lines)

        with codecs.open(os.path.join(dst, filename), "w", encoding="utf8") as f:
            f.write(new_text)


def add_chapters(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for filename in os.listdir(src):
        with codecs.open(os.path.join(src, filename), "r", encoding="utf8") as f:
            text = f.read()
        new_text = "<chapter>\n"+text+"\n</chapter>\n"

        with codecs.open(os.path.join(dst, filename), "w", encoding="utf8") as f:
            f.write(new_text)


def replace_strange_characters(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for filename in os.listdir(src):
        with codecs.open(os.path.join(src, filename), "r", encoding="utf8") as f:
            text = f.read()
            new_text = text.replace("&c.", "")

        with codecs.open(os.path.join(dst, filename[:-3]+"xml"), "w", encoding="utf8") as f:
            f.write(new_text)


def add_word_tag(src, dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
    for filename in os.listdir(src):
        tree = etree.ElementTree()
        tree.parse(os.path.join(src, filename))
        for entry in tree.iter("entry"):
            for line in entry:
                if line.tag == "word":
                    word = clean("".join(line.itertext()))
                    entry.set("word", word)
                    entry.remove(line)

        tree.write(os.path.join(dst, filename[:-3]+"xml"), encoding="utf8")


def first_step():
    src = "original_dict"
    dst_transform = "1"
    transform(src, dst_transform)

    src_mi = dst_transform
    dst_mi = "2"
    transform_mi(src_mi, dst_mi)

    src_word_tag = dst_mi
    dst_word_tag = "3"
    give_word_tag(src_word_tag, dst_word_tag)

    src_remove_double_tag = dst_word_tag
    dst_remove_double_tag = "4"
    remove_double_tab(src_remove_double_tag, dst_remove_double_tag)


def second_step():
    dst = "entries"
    src_change_name_mark = "entries_before_change_name_mark"
    dst_change_name_mark = "5"
    change_name_mark(src_change_name_mark, dst_change_name_mark)

    src_add_chapters = dst_change_name_mark
    dst_add_chapters = "6"
    add_chapters(src_add_chapters, dst_add_chapters)

    src_replace_strange_characters = dst_add_chapters
    dst_replace_strange_characters = "7"
    replace_strange_characters(src_replace_strange_characters, dst_replace_strange_characters)

    add_word_tag(dst_replace_strange_characters, dst)


def merge_files(src, dst_filename):
    texts = []
    for filename in os.listdir(src):
        with codecs.open(os.path.join(src, filename), "r", encoding="utf8") as f:
            text = f.readlines()
            texts.append("\n".join(text[1:-1]))
            # ElementTree.fromstringlist(text)
    with codecs.open(""+dst_filename, "w", encoding="utf8") as f:
        f.write("<?xml version='1.0' encoding='utf8'?>\n<dictionary>\n"+"".join(texts)+"\n</dictionary>")


def from_xml_to_yaml(filename_src, filename_dst):
    """
    >>> from_xml_to_yaml("dictionary.xml", "dictionary.yaml")

    :param filename_src:
    :param filename_dst:
    :return:
    """
    parser = etree.XMLParser()
    tree = etree.parse(filename_src, parser=parser)
    d = {}
    for entry in tree.findall(".//entry"):
        # print(entry.get("word"))
        # print(etree.tostring(entry))
        # print(BeautifulSoup(etree.tostring(entry)).text)
        # print(BeautifulSoup(etree.tostring(entry), features="lxml").contents)
        # print([child for child in BeautifulSoup(etree.tostring(entry), features="lxml").children])
        # print(BeautifulSoup(etree.tostring(entry), features="lxml").stripped_strings)
        d[entry.get("word")] = BeautifulSoup(etree.tostring(entry), features="lxml").text.strip()  # ElementTree.tostring(entry).decode("utf-8")

    with open(filename_dst, "w", encoding="utf-8") as f:
        yaml.safe_dump(d, f, )


def read_yaml(filename):
    """
    >>> read_yaml("dictionary.yaml")["sonr"]

    :param filename:
    :return:
    """
    with open(filename, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=yaml.CLoader)


if __name__ == "__main__":
    # From http://norroen.info/dct/zoega
    first_step()
    # manual annotation
    # "5" directory is renamed "entries_before_change_name_mark"
    second_step()

    merge_files("entries", "dictionary.xml")
