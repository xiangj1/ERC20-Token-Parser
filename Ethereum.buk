from html.parser import HTMLParser
from urllib.request import Request, urlopen
import pandas as pd
import time

class wallet_info(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.round = 0
        self.inTbody = 0
        self.isTd = 0

    def handle_starttag(self, tag, attrs):
        if(tag == 'tbody'):
            self.inTbody = 1
        if(tag == 'td' and self.inTbody == 1):
            self.isTd = 1

    def handle_endtag(self, tag):
        if(tag == 'tbody'):
            self.inTbody = 0
        if(tag == 'td'):
            self.isTd = 0

    def handle_data(self, data):
        if(self.isTd == 1):
            self.round += 1
            daf.append(data.replace(",", "").replace(" Ether", ""))

#global variable
start = time.time()
daf = []
Rank = []
Wallet_Address = []
Quantity = []
Percentage = []

url = 'https://etherscan.io/accounts/1?ps=50'
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
parser = wallet_info()


parser.feed(str(webpage))
j = 0
for k in range(0, 10000):
    try:
        if(daf[j] == " "):
            del daf[j]
        elif('|' in daf[j]):
            del daf[j]
        elif(daf[j+1] == '.'):
            daf[j] = str(daf[j])+str(daf[j+1])+str(daf[j+2])
            del daf[j+1]
            del daf[j+1]
        else:
            j += 1
    except IndexError:
        break

for i in range(0, len(daf)):
    print(i, daf[i])

for l in range(0, 100):
    try:
        Rank.append(daf[l*5])
        Wallet_Address.append(daf[l*5+1])
        Quantity.append(daf[l*5+2])
        Percentage.append(daf[l*5+3])
    except IndexError:
        break
df = pd.DataFrame({'Rank': Rank, 'Wallet_Address': Wallet_Address,
                   'Quantity': Quantity, 'Percentage': Percentage})
df.to_csv("token_wallet_Ethereum.csv")


end = time.time()
print("Time Used(in seconds):")
print(end - start)
