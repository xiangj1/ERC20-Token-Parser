import csv
import sys
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import numpy as np

chrome_path =r"C:\Users\admin\Desktop\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)


#url2 = 'https://etherscan.io/token/generic-tokenholders2?a=%s&p=%d&s=%s'%("ssss",3,"s")


df = pd.read_csv('tokeninfo.csv',header=None)
url = 'https://etherscan.io/tokens?p=1'
driver.get(url)
driver.maximize_window()

for i in range(1,501):
    addressinfo = "address_%s.csv"%(df[0][i])
    with open(addressinfo, 'w') as f:
        f.write("rank,address,quantity,percentage \n")
    for j in range(1,21):
        url = 'https://etherscan.io/token/generic-tokenholders2?a=%s&p=%d&s=%d'%(df[2][i],j,int(df[1][i])*10**int(df[3][i]))
        driver.get(url)
        for k in range(2,52):
            try:
                rank = driver.find_element_by_xpath('//*[@id="maintable"]/table/tbody/tr['+str(k)+']/td[1]')\
                   .text.replace(',','').encode('utf-8').decode('utf-8')
            except NoSuchElementException:
                rank = "unknown"
            try:
                address = driver.find_element_by_xpath('//*[@id="maintable"]/table/tbody/tr['+str(k)+']/td[2]/span/a')\
                   .text.replace(',','').encode('utf-8').decode('utf-8')
            except NoSuchElementException:
                address = "unknown"
            try:
                quantity = driver.find_element_by_xpath('//*[@id="maintable"]/table/tbody/tr['+str(k)+']/td[3]')\
                   .text.replace(',','').encode('utf-8').decode('utf-8')
            except NoSuchElementException:
                quantity = "unknown"
            try:
                percentage = driver.find_element_by_xpath('//*[@id="maintable"]/table/tbody/tr['+str(k)+']/td[4]')\
                   .text.replace(',','').encode('utf-8').decode('utf-8')
            except NoSuchElementException:
                percentage = "unknown"
            with open(addressinfo, 'a') as f:
                f.write(str(rank)+ "," + str(address) +"," +str(quantity)+","+str(percentage))
                f.write('\n')
                f.close()
    

