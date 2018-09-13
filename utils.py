"""

"""

import os
import codecs


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
        # text = text.replace("[", "<")
        # text = text.replace("]", ">")
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
                # for i in range(1, 6):
                #     if "<m"+str(i)+">" in line:
                #         line_length = len(line)
                #         line = line[:line_length-6]
                #         line += "</m"+str(i)+">"
                lines.append(line)
        text = "\n".join(lines)+"\n</word>"
        text = "\n".join(text.split("\n")[1:])
        # text = text.replace("[", "<")
        # text = text.replace("]", ">")
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


if __name__ == "__main__":
    # transform()
    # transform_mi()
    # give_word_tag()
    remove_double_tab()
