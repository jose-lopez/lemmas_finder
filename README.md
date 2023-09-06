# lemmas_scraper
A jupyter notebook for the web scraping of lemmas related to ancient greek words.

This notebook processes the *.csv files located in the text/corpus folder, 
producing updated versions of them, stored in a folder named
"processed". Files with warnings and logs are also generated for
each one of the *.csv files.

For instance, if you have some lines in one of the .csv files, like these:

  n token lemma pos
0	1	Ζεὺς	Ζεύς	n-s---mn-
1	2	μὲν	μέν	g--------
2	3	ἀφίκτωρ	ἀφίκτωρ	n-s---mn-
3	4	ἐπίδοι	ἐφοράω	v3saoa---
4	5	προφρόνως	πρόφρων	d--------
5	1	στόλον	στόλος	n-s---ma-
6	2	ἡμέτερον	ἡμέτερος	a-s---ma-
7	3	νάιον	νήϊος	a-s---ma-
8	4	ἀρθέντʼ		a-s---ma-

then, the goal of the code is to scrap the best lemma available from those 
tokens lacking one. The lemmas are scraped from web site:
https://logeion.uchicago.edu/morpho/.

A file of the type "warnings" informs about possible syntactical errors
in tokens in the input files.

A "log" type file, on the other hand, reports problems found when trying
to access a URL, for a given token.

The text/processed folder also includes files listing all the new lemmas
found for each token in each one of the input files.

This repo also includes a python script version at: ./src/scraping/lemmas.py

