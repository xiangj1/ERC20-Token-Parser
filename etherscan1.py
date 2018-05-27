import csv
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

chrome_path =r"C:\Users\admin\Desktop\chromedriver.exe"
driver = webdriver.Chrome(chrome_path)

url = 'https://etherscan.io/tokens?p=1'
driver.get(url)
driver.maximize_window()

with open('tokeninfo.csv', 'w') as f:
    f.write("name,total_supply,address,decimals \n")

for p in range(1,501):
    for i in range(1,51):
        url = 'https://etherscan.io/tokens?p=%d'%(p)
        driver.get(url)
        try:     
            driver.execute_script("arguments[0].click();",\
            driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_divresult"]/table/tbody/tr['+str(i)+']/td[3]/h5/a'))
        except NoSuchElementException:
            break
        try:
            name = driver.find_element_by_xpath('//*[@id="address"]')\
                   .text.replace(',','').encode('utf-8').decode('utf-8')
        except NoSuchElementException:
            name = "unknown"
        try:
            total_supply = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_divSummary"]/div[1]/table/tbody/tr[1]/td[2]')\
                   .text.replace(',','').encode('utf-8').decode('utf-8').split()[0]
        except NoSuchElementException:
            total_supply = "unknown"
        try:
            address = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_trContract"]/td[2]/a')\
                   .text.replace(',','').encode('utf-8').decode('utf-8')
        except NoSuchElementException:
            address = "unknown"
        try:
            decimals = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_divSummary"]/div[2]/table/tbody/tr[2]/td[2]')\
                   .text.replace(',','').encode('utf-8').decode('utf-8') 
        except NoSuchElementException:
            decimals = "unknown"
                                                  
        with open('tokeninfo.csv', 'a') as f:
            f.write(str(name)+ "," + str(total_supply) +"," +str(address)+","+str(decimals))
            f.write('\n')
            f.close()
        driver.get(url)
        
 
    

