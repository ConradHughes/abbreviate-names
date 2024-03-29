# abbreviate-names

Uniquely abbreviate a set of names in a language-appropriate way.
The original intent was to shorten a collection of Latin species names
such that they would fit more nicely into tables and graphs, but other
applications abound!

This packages provides both

* **a programmatic API**, `names.abbreviate.abbreviate()` and
* **a command line tool**, `abbreviate-names`.

If installed with English or Latin options it also includes dependencies
on natural language modules which enable it to break names up at
syllable boundaries, which produces more readable results.

# Example output

Species | Abbreviation using Latin syllables | .. or by character
------------ | ------------ | --
Agathidium laevigatum | Agat.lae. | A.l.
Agathidium nigrinum | Agat.nigrinum | A.nigrin.
Agathidium nigripenne | Agat.nigripen. | A.nigrip.
Agathidium seminulum | Agat.se. | A.s.
Agonum ericeti | Ago.e. | A.e.
Agonum fuliginosum | Ago.fu. | A.f.
Agonum gracile | Ago.gra. | A.g.
Lithocharis sp. | Lit.sp. | L.sp.
Xylocleptes bispinus | Xy.bis. | X.b.
Xylodromus concinnus | Xy.con. | X.c.
Xylodromus depressus | Xy.de. | X.d.
Xylostiba monilicornis | Xy.mo. | X.m.
Zeugophora subspinosa | Zeu.sub. | Z.s.

Observe:

* Several different words above are all shortened to “Xy.” or “X.” —
it's the whole abbreviation that's unique, not the individual words.
* The already-abbreviated “sp.” is untouched.

# Getting started

```shell

    $ pip install cltk==0.1.121    # For Latin; haven't updated to current CLTK
    $ pip install 'abbreviate-names[Latin,English]'

    $ cat test.csv                 # Note first line is column name
    taxa
    Cicindela campestris
    Cychrus caraboides
    Carabus granulatus
    Carabus nemoralis
    Carabus nitens
    Carabus problematicus
    Carabus violaceus
    Leistus ferrugineus
    Leistus fulvibarbis

    $ abbreviate-names --latin test.csv
    taxa,Abbreviation
    Cicindela campestris,Ci.cam.
    Cychrus caraboides,Cyc.ca.
    Carabus granulatus,Ca.gra.
    Carabus nemoralis,Ca.ne.
    Carabus nitens,Ca.ni.
    Carabus problematicus,Ca.pro.
    Carabus violaceus,Ca.vi.
    Leistus ferrugineus,Leis.fer.
    Leistus fulvibarbis,Leis.ful.

```

# Online

* **GitHub:** https://github.com/ConradHughes/abbreviate-names
* **PyPI:** https://pypi.org/project/abbreviate-names/
