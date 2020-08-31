"""Given a list of (multiword) names, produce a set of uniquely identifying abbreviations, usually using a language model to break them nicely at syllable boundaries.
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

import csv
import argparse
from pathlib import Path
import sys

from names.abbreviate import abbreviate

def main(args=None):
    ap = argparse.ArgumentParser(description=__doc__, epilog="Default is to syllabify using nltk, which may be based on English, or perhaps on your locale (not quite sure!).  Using a syllabifier to break the words ensures more pronounceable abbreviations, though they'll be longer too.  With --by-character the abbreviations will be very short, but not so easy to make sense of.  Any words in the name list that already end in '.' will be treated as canonical abbreviations, and not modified.  Where an \"abbreviation\" uses a whole word, no trailing '.' will be used for that word; hence the list [\"abbreviate\", \"ab\"] will produce abbreviations [\"ab.\", \"ab\"] (note distinguishing '.').")
    ap.add_argument('-c', '--by-character', action='store_true', help="Don't syllabify: just use as few characters as posssible.")
    ap.add_argument('-l', '--latin', action='store_true', help="Use a Latin language model for syllabification.")
    ap.add_argument('input_csv', nargs='?', type=argparse.FileType('r'), help='Single-column CSV of names to abbreviate (a first-line column title is expected).  Defaults to stdin.', default=sys.stdin)
    ap.add_argument('output_csv', nargs='?', type=argparse.FileType('w'), help='CSV to write to.  Will contain two columns: both original names and abbreviations.  Defaults to stdout.', default=sys.stdout)

    args = ap.parse_args()

    if args.latin: # Latin
        if args.by_character:
            sys.exit("'--latin' and '--by-character' don't make sense together!")
        import os
        cltk_dir = Path('cltk_data')
        # Keep cltk_data directory local.
        os.environ['CLTK_DATA'] = str(cltk_dir)
        cltk_dir.mkdir(exist_ok=True)
        print("Getting/updating Latin corpus; might take a minute!",
                file=sys.stderr)
        from cltk.corpus.utils.importer import CorpusImporter
        from cltk.stem.latin.syllabifier import Syllabifier
        corpus_importer = CorpusImporter('latin')
        corpus_importer.import_corpus('latin_text_latin_library')
        syllabifier = Syllabifier().syllabify
    elif not args.by_character:
        # English - or maybe whatever your locale specifies, not sure..
        from nltk.tokenize import SyllableTokenizer
        tk = SyllableTokenizer()
        syllabifier = tk.tokenize

    # Seems overkill to use a CSV reader for one column, but (for example) this
    # makes it easy to correctly read in a possibly-quoted exported column from
    # a spreadsheet.
    reader = csv.reader(args.input_csv)
    # The conditional here is to cope with empty rows.
    column, *names = [row[0] if len(row) == 1 else '' for row in
            list(reader)]

    abbrs = abbreviate(names, breaker=syllabifier) if 'syllabifier' in locals() else abbreviate(names)

    # Write CSV to stdout.
    out = csv.writer(args.output_csv, lineterminator='\n')
    names = [[name, abbrs[name]] for name in names]
    out.writerows([[column, 'Abbreviation'], *names])

if __name__ == "__main__":
    sys.exit(main() or 0)
