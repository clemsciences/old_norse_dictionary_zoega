# Old Norse Dictionary Zoega
Zoëga's A Concise Dictionary of Old Icelandic parser

With the **reader.py** module, you can:

* search a word with an edit distance below a given threshold,
* extract the POS tags in dictionary entries,
* search for exact entry and approximate entry.

However POS tag extractor is not very efficient. More special cases need to be handled.

TODO list:
* [x] look up a word in dictionary
* [x] search all words in dictionary which are at most at a given edit distance with the query word
* [ ] handle more dictionary entry,
* [ ] process all entries so that we would get virtually all the Old Norse words,
* [ ] for each form, we can associate lemmata with a proposed POS tag.

## Elaboration of data

Data come from https://github.com/GreekFellows/lesser-dannatt and http://norroen.info/dct/zoega by Tim Ermolaev.
Then `utils.first_step()` is launched. I modified the files in order to ensure 
XML syntax consistency, finally `utils.second_step()` is launched.
