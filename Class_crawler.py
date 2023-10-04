#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 27 18:12:56 2018

@author: hannina
"""

#Scraping website

import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import re

def getsource(url):
    req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}) #sends GET request to URL
    uClient=urllib.request.urlopen(req)
    page_html=uClient.read() #reads returned data and puts it in a variable | could use .decode('utf-8')
    uClient.close() #close the connection
    page_soup=BeautifulSoup(page_html,"lxml")
    return [page_soup, page_html]

baseUrl = r'https://www.amazon.com/s/ref=nb_sb_noss_2?'
searchQuery = 'field-keywords=' #enter search terms "+" 
queryFile = '/Users/hannina/Documents/IS-Python/searchTerms.txt'

#Opening the file specified as "variable name you specify"
#Anything you do inside that with block
#Works with the file open
#LEaving the with block, automatically closes the file

with open(queryFile) as f:
    searchTerms = f.read().splitlines()
    
for term in searchTerms:
    url = baseUrl + searchQuery + urllib.parse.quote_plus(term)
    pageData = getSource(url)
    searchPage = pageData[0]
    # //div[@id="atfResults"]//div[@class="s-item-container"]
    for product in searchPage.find('div',{'id': 'atfResults'}).findAll('div',{'class': 's-item-container'})
    print(product.find('div', {'class': 'a-row a-spacing-small'}).find('h2').get('data-attribute'))#returns the outer element

print(searchTerms)