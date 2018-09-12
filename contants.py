"""
Constants to read dictionary entries
"""


abbreviations = {
    "a.": "adjective",
    "absol.": "absolute, absolutely",
    "acc.": "accusative",
    "adv.": "adverb",
    "card. numb.": "cardinal number",
    "Cf.": "confer",
    "cf.": "confer",
    "compar.": "comparative",
    "compds.": "compounds",
    "conj.": "conjunction",
    "dat.": "dative",
    "def. art.": "definite article",
    "dem. pron.": "demonstrative pronoun",
    "e-a": "einhverja",
    "e-m": "einhverjum",
    "e-n": "einhvern",
    "e-rra": "einhverra",
    "e-rri": "einhverri",
    "e-s": "einhvers",
    "e-t": "eitthvert",
    "e-u": "einhverju",
    "esp.": "especially",
    "f.": "feminine noun",
    "for.": "foreign",
    "fem.": "feminine",
    "freq.": "frequent, frequently",
    "gen.": "genitive",
    "i. e.": "id est",
    "imperat.": "imperative",
    "impers.": "impersonal",
    "indecl.": "indeclinable",
    "indef. pron.": "indefinite pronoun",
    "infin.": "infinitive",
    "int. pron.": "interrogative pronoun",
    "interj.": "interjection",
    "m.": "masculine noun",
    "masc.": "masculine",
    "n.": "neuter noun",
    "neut.": "neuter",
    "nom.": "nominative",
    "ord. numb.": "ordinal number",
    "pers. pron.": "personal pronoun",
    "pl.": "plural",
    "poet.": "poetically",
    "poss. pron.": "possessive pronoun",
    "pp.": "past participle",
    "pr. p.": "present participle",
    "prep.": "preposition",
    "pron.": "pronoun",
    "recipr.": "reciprocally",
    "refl.": "reflexive",
    "refl. pron.": "reflexive pronoun",
    "rel. pron.": "relative pronoun",
    "sing.": "singular",
    "superl.": "superlative",
    "v.": "verb",
    "v. refl.": "reflexive verb",
    "viz.": "namely"
}

oums = ["ǫ", "ö", "ø"]

heads = [
    "a", "á", "æ", "b", "d",
    "e", "f", "g", "h", "i",
    "í", "j", "k", "l", "m",
    "n", "o", "œ", "ó", oums[0],
    "p", "r", "s", "t", "þ",
    "u", "ú", "v", "y", "ý"
]

headDictPaths = [
    "dict/a.dsl", "dict/aa.dsl", "dict/ae.dsl", "dict/b.dsl", "dict/d.dsl",
    "dict/e.dsl", "dict/f.dsl", "dict/g.dsl", "dict/h.dsl", "dict/i.dsl",
    "dict/ii.dsl", "dict/j.dsl", "dict/k.dsl", "dict/l.dsl", "dict/m.dsl",
    "dict/n.dsl", "dict/o.dsl", "dict/oe.dsl", "dict/oo.dsl", "dict/oum.dsl",
    "dict/p.dsl", "dict/r.dsl", "dict/s.dsl", "dict/t.dsl", "dict/th.dsl",
    "dict/u.dsl", "dict/uu.dsl", "dict/v.dsl", "dict/y.dsl", "dict/yy.dsl"
]
