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


if __name__ == "__main__":
    transform()
