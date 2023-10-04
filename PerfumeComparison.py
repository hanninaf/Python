#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 19:49:05 2018

@author: hannina
"""


# USER INPUT
import re
from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
from time import sleep   
 #if user use spaces, replace with +
def urlify(s):
     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)
     # Replace all runs of whitespace with a plus
     s = re.sub(r"\s+", '+', s)
     return s
product = input("Product's name: ")
nameProduct = urlify(product)

brand = input("Brand's name: ")

listGender = ["Male","Female","male","female","M","F","m","f","N/A","n/a","na",""]
while True:
    gender = input("Gender (Male or Female): ")
    if gender not in listGender:
        print("Invalid input")
        continue
    else:
        break
if (gender=='m'):
    gender='Male'
elif (gender=='f'):
    gender='Female'
elif gender in ("N/A","n/a","na",""):
    gender='None'

while True:
    val1 = input("Quantity: ")
    try:
        count = int(val1)
        if count <= 0:
            print("Invalid input")
            continue
        else:
            break
    except ValueError:
        print("Invalid input")

ozlist = ["0.17","0.5","0.8","1","1.4","1.7","2","2.5","2.7","3","3.4","4.2"]
ozchart = [float(i) for i in ozlist]
mllist = ["5","15","25","30","40","50","60","75","80","90","100","125"]
mlchart = [float(i) for i in mllist]
sizechart = [ozchart,mlchart]
while True:
    val2 = input("Size (fl oz or ml): ")
    try:
        size = float(val2)
        if (size not in ozchart and size not in mlchart):
            print("Invalid input")
            continue
        else:
            break
    except ValueError:
        print("Invalid input")


print('\n')
print('Find '+product.title()+' by '+brand.title()+' for '+gender.title()+' size '+str(size)+' quantity '+str(count)+'\n')

# LISTING SITES AND PRICES
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def ensAbs(url):
    if bool(urllib.parse.urlparse(url).netloc):    
        return url
    else:
        return urllib.parse.urljoin(startURL,url)

def getSource(url):
    req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}) #sends GET request to URL
    uClient=urllib.request.urlopen(req)
    page_html=uClient.read().decode('utf8') #reads returned data and puts it in a variable
    uClient.close() #close the connection
    page_soup=BeautifulSoup(page_html,'lxml')
    return [page_soup, page_html]

# This is our starting point, in this case a google search string
startURL =  r'https://www.google.com/search?output=search&tbm=shop&q='

#nameProduct = urlify(input("Product's name: "))
myURL = startURL + nameProduct
pageData = getSource(myURL)

myProducts = pageData[0].findAll('div', {'class': 'ZGFjDb'})

myData = []
for item in myProducts:
    products = {}
    products['name'] = item.find('a', {'data-what': '1'}).text.strip()
    name = products['name']
    price = item.find('div', {'class': 'mQ35Be'}).text.strip().strip('$')
    if (re.search(r'stores',price)):
        urlRaw = item.find('a', {'data-what': '1'}).get('href')
        urlGood = ensAbs(urlRaw)
        productPageSoup = getSource(urlGood)[0]
        lists = productPageSoup.findAll('tr',{'class': 'os-row'})
        if lists is not None:
            for i in lists:
                products['name'] = name
                products['seller'] = i.find('span',{'class': 'os-seller-name-primary'}).text.strip()
                priceInList = i.find('td',{'class': 'os-total-col'}).text.strip().strip('$')
                if (priceInList==''):
                    priceInList='0'
                products['price'] = float(priceInList)
                #print(products)
                if (products['price'] != 0):
                    myData.append(products)
                products = {}
    else:
        index = price.index('f')
        products['seller'] = price[index+5:]
        newprice = price[:index]
        products['price'] = float(newprice)
        #print(products)
        if (products['price'] != 0):
            myData.append(products)
        products = {}

print('\n')
print('Here is my data \n')
print(myData)

print('\n')
print('Sorted data \n')
sortedPrice = sorted(myData, key=lambda products: products['price'])
print(sortedPrice)

print('\n')
print('My Result:\n')
print(sortedPrice[0]) 

driver = webdriver.Chrome('/Applications/Google Chrome.app')
driver.get(myURL)
sleep(10)
driver.find_element_by_xpath("//div[@class='goog-inline-block jfk-button jfk-button-standard jfk-button-narrow jfk-button-collapse-left']").click()

while True:
    try:
        for item in myProducts:
            products = {}
            products['name'] = item.find('a', {'data-what': '1'}).text.strip()
            name = products['name']
            price = item.find('div', {'class': 'mQ35Be'}).text.strip().strip('$')
            if (re.search(r'stores',price)):
                urlRaw = item.find('a', {'data-what': '1'}).get('href')
                urlGood = ensAbs(urlRaw)
                productPageSoup = getSource(urlGood)[0]
                lists = productPageSoup.findAll('tr',{'class': 'os-row'})
                if lists is not None:
                    for i in lists:
                        products['name'] = name
                        products['seller'] = i.find('span',{'class': 'os-seller-name-primary'}).text.strip()
                        priceInList = i.find('td',{'class': 'os-total-col'}).text.strip().strip('$')
                        if (priceInList==''):
                            priceInList='0'
                            products['price'] = float(priceInList)
                            #print(products)
                            if (products['price'] != 0):
                                myData.append(products)
                                products = {}
                else:
                    index = price.index('f')
                    products['seller'] = price[index+5:]
                    newprice = price[:index]
                    products['price'] = float(newprice)
                    #print(products)
                    if (products['price'] != 0):
                        myData.append(products)
                        products = {}

        print('\n')
        print('Here is my data \n')
        print(myData)

        print('\n')
        print('Sorted data \n')
        sortedPrice = sorted(myData, key=lambda products: products['price'])
        print(sortedPrice)

        print('\n')
        print('My Result:\n')
        print(sortedPrice[0])
        productPageSoup.find_element_by_xpath("//div[@class='goog-inline-block jfk-button jfk-button-standard jfk-button-narrow jfk-button-collapse-left']").click()
        sleep(5)
        #elm = driver.find_element_by_css_selector('goog-inline-block jfk-button jfk-button-standard jfk-button-narrow jfk-button-collapse-left')
        #elm.click()
            #URL = driver.current_url 
            #driver.get(URL)
            #HTML = driver.page_source
            #cards = BeautifulSoup(HTML,'lxml') 
    except:
        break


