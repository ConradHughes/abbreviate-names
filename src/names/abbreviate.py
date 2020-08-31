"""
Uniquely abbreviate a set of names in a language-appropriate way.
"""

# Copyright (C) 2020 Conrad Hughes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from collections import defaultdict
import functools
import itertools
import warnings

def _prefixes(l):
    if l and l[-1][-1] == '.': # Already an abbreviation
        return [''.join(l)]
    prefixes = [''.join(l[0:i]) + '.' for i in range(1, len(l))]
    prefixes.append(''.join(l))
    return prefixes

def _assemble(p):
    return functools.reduce(lambda a,b: a + b if a[-1] == '.' else a + ' ' + b, p) if p else ''

def abbreviate(names, breaker=list):
    """
    Given a list of strings, return a map from those strings to
    abbreviated versions thereof, such that each abbreviation is the
    shortest that uniquely identifies its full string within the
    provided list.  This was designed to abbreviate sets of Latin
    species names, but will work with essentially anything.

    Default is to break words into individual characters and find
    shortest unique abbreviations based on these: they're very short,
    but not very memorable/speaker-friendly.  Supplying a language-
    appropriate syllable breaker here will produce longer, but much
    nicer, abbreviations.  Example::

        from cltk.corpus.utils.importer import CorpusImporter
        from cltk.stem.latin.syllabifier import Syllabifier
        [..]
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_latin_library')
        syllabifier = Syllabifier()
        [..]
        abbrs = abbreviate(names, breaker=syllabifier.syllabify)

    Any words in the name list that already end in '.' will be treated
    as canonical abbreviations, and not modified.  Where an
    "abbreviation" uses a whole word, no trailing '.' will be used for
    that word; hence you might find "N.vespillo" (an abbreviation for
    "Nicrophorus vespillo") and "N.vespillo." (for "Nicrophorus
    vespilloides" — note the trailing '.') as distinct abbreviations in
    the returned dictionary.  Tried coding a "subtle distinctions" flag
    to disable this behaviour, but identifying the best alternative
    seems non-trivial.
    """
    # Could remove punctuation with
    #   import string
    #   nopunct = str.maketrans('', '', string.punctuation)
    # .. and
    #   name.translate(nopunct)
    counts = defaultdict(int)
    abbrs = {}
    for name in names:
        if name in abbrs:
            warnings.warn('"' + name + '" duplicated.')
            continue
        # Need to generate counts for *all* character-by-character
        # abbreviations since syllable breaks don't always occur in the same
        # places for words that share identical textual prefixes — for example
        # "pericarpius" splits at "pe-", but "perpendicularis" splits at
        # "per-".  Without recording character-by-character abbreviations we
        # could erroneously end up thinking that "pe." is an unambiguous
        # abbreviation for "pericarpus", even though "perpendicularis" is in
        # the same set of words.
        c_all = [_prefixes(list(word)) for word in name.split()]
        for c in itertools.product(*c_all):
            counts[_assemble(c)] += 1
        c_good = [_prefixes(breaker(word)) for word in name.split()]
        c_good = [_assemble(p) for p in itertools.product(*c_good)]
        abbrs[name] = sorted(c_good, key=lambda b: (len(b), b))
    for name, candidates in abbrs.items():
        try:
            abbrs[name] = next(c for c in candidates if counts[c] == 1)
        except StopIteration:
            abbrs[name] = name
    return abbrs
