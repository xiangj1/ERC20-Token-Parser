# This file will extract the token exployer from coinmarketcap,
# if the exployer url is from etherscan, write it in the file

coin_url = 'https://coinmarketcap.com/currencies/'
etherScan_url = 'https://etherscan.io/token/'

import json
import time
import urllib.request
from html.parser import HTMLParser

class CoinExployerAddress(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.exployer = ""
        self.isEtherScan = 0
        return

    def handle_starttag(self, tag, attrs):
        # first detect the a tag, then find the href
        if(tag == 'a'):
            for attr in attrs:
                if(attr[0] == 'href'):
                    self.exployer = attr[1]
        return

    def handle_data(self, data):
        # filter out the exployer address from a tag
        if(data.strip() == "Explorer"):
            # addresses.write(self.exployer + '\n')
            # if the first explorer is from etherscan
            if(self.exployer.find(etherScan_url) != -1):
                self.isEtherScan = 1
            else:
                addresses.write(self.exployer + '\n')
        elif(data.strip() == "Explorer 2" and self.isEtherScan == 1):
                addresses.write(self.exployer + '\n')
                self.isEtherScan = 0

        return 

    def handle_endtag(self, tag):
        return


#starting time
starting_time = time.time()

# load json file
with open('Top100.json') as file:
    top100 = json.load(file)

# initial addresses dict
coin_addresses = dict()

# open the existing address and load it in coin_addresses
with open('coin_addresses.txt', 'r+') as file:
    for line in file:
        (key, value) = line.split(' ')
        coin_addresses[key] = value.strip()

# open the existing address and set as append
addresses = open('coin_addresses.txt', 'a+')

# initial a html parser
exployerGetter = CoinExployerAddress()

# for each coin in the json file
#   make a request to the detail website
#   then get the explorer address
for coin in top100['data']:
    if(coin_addresses.get(coin['symbol']) == None):
        coin_request = urllib.request.Request(coin_url + coin['website_slug'] + '/', headers={'User-Agent': 'Mozilla/5.0'})
        tem_str = str(urllib.request.urlopen(coin_request).read())
        addresses.write(coin['symbol'] + ' ')
        exployerGetter.feed(tem_str)

print("GetCoinExplorer.py DONE at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "\t Cost: " + str(time.time() - starting_time))
    