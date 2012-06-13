sentence_checker
================

Sentence checker for Chinese Learners of English (CLE)

This is a python spell-checker-like sentence corrector. 
Made for English Learners especially whoes mother-tongue is Chinese.

It can correct most none-word errors and some real-word errors and syntax errors usually made by CLE, 
such as typo (form, from), tense (she was, she were), single/plural (two questions, two question), 
set phrase (she is very beautiful, she is very beautifully) ...

The core correcting system is based on the LM made from ChinaDaily/Reuters corpus, and the unique CLE confusion set.

Nmgram probalibity checker, Tag probability checker.