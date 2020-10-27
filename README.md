# gsr
Quantifying Gender Stereotype Reinforcement in Search Engines

Begin by building toy datasets, then run gsr_computation onto them.

The core function is utils.txt_file_avg_genderedness, which computes the average projection of words in a txt file along a specified direction.

Fixes with respect to https://doi.org/10.1016/j.ipm.2020.102377:
- "him" is added as a gendered stop word that should be considered for genderedness computation of a text file.

Requires google_news_vectors_negative_300.bin, available at https://code.google.com/archive/p/word2vec/
Uses we.py from https://github.com/tolga-b/debiaswe