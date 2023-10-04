#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 18:31:58 2018

@author: hannina
"""

import nltk, re, pprint
from nltk import word_tokenize
from nltk.corpus import stopwords

wnl = nltk.WordNetLemmatizer()

with open(r'.txt') as file:
    EM_raw = file.read()
EM_token = word_tokenize(EM_raw.lower())
EM_token_clean = [t for t in EM_token if re.match(r'[^\W\d]*$', t)]
