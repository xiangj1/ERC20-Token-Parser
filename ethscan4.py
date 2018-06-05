from html.parser import HTMLParser
from urllib.request import Request, urlopen
import pandas as pd
import numpy as np
import time

start = time.time()
token = []
address = []
total_supply = []
decimals = []
token_n = []
contract_address = []

class erc20_token_list(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.isname = 0
        self.inh5 = 0
        self.inTbody = 0

    def handle_starttag(self, tag, attrs):
        if(tag == 'tbody'):
            self.inTbody = 1
        if(tag == 'h5'):
            self.inh5 = 1   
        if(tag == 'a' and self.inTbody == 1 and self.inh5 == 1):
            for name, value in attrs:
                if (name == 'href'):
                    self.isname = 1
                    address.append(value.split("/")[2].split('\\')[0])

    def handle_endtag(self, tag):
        if(tag == 'tbody'):
            self.inTbody = 0
        if(tag == 'h5'):
            self.inh5 = 0
        if(tag == 'a'):
            self.isname = 0

    def handle_data(self, data):
        if(self.isname == 1):
            token.append(data[data.find("(")+1:data.find(")")])


class token_fixed_info(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.inTable = 0
        self.round = 0
        self.istd =0
        self.r = 0
        self.t = 0
        self.a = 0
        self.f  = 0
    
    def handle_starttag(self, tag, attrs):
        if (tag == 'table'):
            for name, value in attrs:
                if(name == 'class' and value =='table'):
                    self.inTable =1
        if (tag == 'td' and self.inTable ==1):
            self.istd =1
            
    def handle_endtag(self,tag):
        if(tag =='table'):
            self.inTable = 0
        if(tag == 'td'):
            self.istd =0

    def handle_data(self, data):
        if(self.istd == 1):
            self.round += 1
            if(self.round ==3):
                try:
                    total_supply.append(data.replace(",","").replace("\\n","").split(" ")[0])
                    token_n.append(data.replace(",","").replace("\\n","").split(" ")[1])
                except IndexError:
                    token_n.append(data)
            if ('Decimals:' in data):
               self.r = 1
            if ('Contract:' in data):
               self.a = 1
        if(self.istd ==1 and self.r == 1):
            self.t += 1
            if (self.t ==2):
                decimals.append(data.replace("\\n",""))
        if(self.istd ==1 and self.a == 1):
            self.f += 1
            if (self.f ==3):
                contract_address.append(data)

class wallet_info(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.round = 0
        self.isTd = 0

    def handle_starttag(self, tag, attrs):
        if(tag == 'td'):
            self.isTd = 1

    def handle_endtag(self, tag):
        if(tag == 'td'):
            self.isTd = 0

    def handle_data(self, data):
        if(self.isTd == 1):
            self.round += 1
            for i in range(0,50):   
                if(self.round ==int(i*4)+1):
                    Rank.append(data)
                elif(self.round ==(i*4)+2):
                    Wallet_Address.append(data)
                elif(self.round ==(i*4)+3):
                    Quantity.append(data)
                elif(self.round ==(i*4)+4):
                    Percentage.append(data)

        

for i in range(1,15):
    url1= 'https://etherscan.io/tokens?p='+ str(i)
    req = Request(url1, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    parser = erc20_token_list() 
    parser.feed(str(webpage))


for j in range(0,len(token)):
    url2 = 'https://etherscan.io/token/' + str(address[j])
    req = Request(url2, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    parser = token_fixed_info() 
    parser.feed(str(webpage))

table = pd.DataFrame({'Token':token_n,'Address':contract_address,'Total_Supply':total_supply,'Decimals':decimals})
end = time.time()
print("Time Used(in seconds):")
print(end - start)

question = input("Press y to continue: ")
for a in range(1,100):
    if (question == 'y'):
        start1 = time.time()
        for k in range(0,len(token_n)): 
            Rank = []
            Wallet_Address=[]
            Quantity = []
            Percentage = []
            for j in range(1,21):    
                url3 = 'https://etherscan.io/token/generic-tokenholders2?a=%s&p=%d&s=%s'%(table.loc[k][0],j,int(table.loc[k][3])*10**int(table.loc[k][1]))
                req = Request(url3, headers={'User-Agent': 'Mozilla/5.0'})
                webpage = urlopen(req).read()
                parser = wallet_info()
                parser.feed(str(webpage))
            df = pd.DataFrame({'Rank':Rank,'Wallet_Address':Wallet_Address,'Quantity':Quantity,'Percentage':Percentage})
            df.to_csv("token_wallet_%s.csv"%(table.loc[k][2])) 
        end1 = time.time()
        print("Time Used(in seconds):")
        print(end1 - start1)
        break
