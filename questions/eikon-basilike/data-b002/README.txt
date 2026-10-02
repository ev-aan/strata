Strata bounty B-002 (Eikon Basilike) - test DT-B1 run files, 2026-10-01.

Texts: EEBO-TCP hand-keyed transcriptions, https://github.com/textcreationpartnership/<ID>
  Eikon Basilike, first issue ........ A38258
  Charles I, Kings Cabinet Opened .... A31932 (his own letters only; see KEEP in corpora.py)
  Charles I / Henderson, Newcastle ... A78958 (papers signed "C. R." = Charles; others = Henderson)
  Gauden (13 secure works) ........... A42489 A42498 A42492 A42483 A42487 A42490 A42495 A42475 A42477 A42491 A42496 A42479 A42476
  Taylor ............................. A13414 A27805 A63653 A63711 (letter A63729 used only as a genre check)
  Milton, Eikonoklastes .............. A50898
  Sidney, Arcadia (1590) ............. A12229 ; 1687 Works (captivity prayer) A31771
  Control divines .................... A45397 A57134 A01344 A02549 A64646 A62025 A26864 A31927
Plus Bruce (ed.), Charles I in 1646 (Camden Society 1856), Internet Archive charlesiinlette00chargoog (_djvu.txt).

Run order (from a folder holding the TCP clones and the IA text):
  corpora.py -> corpora.json ; charles1646.py -> charles1646.json
  delta.py (first run)            -> dtb1_results.txt
  genre_check.py                  -> genre_check.txt
  genre_matched.py                -> dtb1b_results.txt
  attractor_check.py              -> attractor_check.txt
  verification.py (main result)   -> verification.txt
  pamela_control.py               -> pamela_control.txt
Seeds fixed; method: Burrows' Delta on the 150 most frequent words after spelling normalisation.
Licence: code MIT, outputs CC BY 4.0.
