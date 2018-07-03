# This file would extract the top50 holders and percentage
# from the coins that given by file 'coin_addresses.txt'

#initial the url and api
total_supply_api = 'https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress='
token_top50_url = 'https://etherscan.io/token/generic-tokenholders2?a='

from html.parser import HTMLParser
import urllib.request
import time

class TokenTop50Parser(HTMLParser):
    def __init__(self, token_symbol):
        HTMLParser.__init__(self)
        self.round = 0
        self.isTd = 0
        self.file = open("CoinData/" + token_symbol + ".json", "w+")
        self.file.write("[")

    def handle_starttag(self, tag, attrs):
        if(tag == 'td'):
            self.isTd = 1

    def handle_endtag(self, tag):
        if(tag == 'td'):
            self.isTd = 0
        elif(tag == 'table'):
            self.file.write('{\"timestamp\":\"' + str(int(time.time())) + '\"}]')

    def handle_data(self, data):
        if(self.isTd == 1):
            self.round += 1
            if(self.round == 1):
                self.file.write("{\"rank\":\"" + data + "\",")
            elif(self.round == 2):
                self.file.write("\"address\":\"" + data + "\",")
            elif(self.round == 3):
                self.file.write("\"amount\":\"" + data + "\",")
            elif(self.round == 4):
                self.file.write("\"percentage\":\"" + data + "\"},")
                self.round = 0


#starting time
starting_time = time.time()

token_supply = dict()
with open("token_supply.txt", "r+") as token_supply_file:
    for line in token_supply_file:
        (key,value) = line.split(" ")
        token_supply[key] = value.strip()

token_supply_file = open("token_supply.txt", "a+")

with open('coin_addresses.txt', 'r') as coin_addresses:
    index = 0
    for line in coin_addresses: #for each coin, detect if it is from etherscan
        (symbol, address) = line.split(' ')

        # if it is a token from etherscan
        identifier = 'ethplorer.io/address/'
        if(address.find(identifier) != -1): 
            index += 1
            # get token address
            # print(symbol, end = '\t')
            address = address.strip()
            token_address = address[address.find(identifier)+len(identifier):]
            # print(str(index) + '. ' + token_address, end = ' ')
            

            # get total supply of the token
            token_total_supply = token_supply.get(token_address) 

            #if token supply is unknown, get from api
            if(token_total_supply == None):
                supply_request = urllib.request.Request(total_supply_api + token_address, headers={'User-Agent': 'Mozilla/5.0'})
                tem_str = str(urllib.request.urlopen(supply_request).read())

                token_total_supply = tem_str[tem_str.index("result")+9:-3]
                # print(token_total_supply) # total supply

                token_supply[token_address] = token_total_supply #store in dictionary
                token_supply_file.write(token_address + " " + token_total_supply + "\n") #write in file
            
            #if supply is known
            # else:
                # print("Cache:" + token_total_supply)

            # get top50 holders from etherscan
            token_top50_request = urllib.request.Request(token_top50_url + token_address + "&s=" + token_total_supply, headers={'User-Agent': 'Mozilla/5.0'})
            tem_str = str(urllib.request.urlopen(token_top50_request).read())

            tokenTop50Parser = TokenTop50Parser(symbol)
            tokenTop50Parser.feed(tem_str)


print("EtherScan.py DONE at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "\t Cost: " + str(time.time() - starting_time))