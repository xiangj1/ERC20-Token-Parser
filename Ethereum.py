from html.parser import HTMLParser
import urllib.request
import time

url = 'https://etherscan.io/accounts/1?ps=25'

class wallet_info(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.round = 0
        self.inTbody = 0
        self.isTd = 0

        self.file = open('CoinData/ETH.json', "w+")
        self.file.write('[')

    def handle_starttag(self, tag, attrs):
        if(tag == 'tbody'):
            self.inTbody = 1
        elif(tag == 'td' and self.inTbody == 1):
            self.isTd += 1
            if(self.isTd == 1): #rank
                self.file.write('{\"rank\":')
                # print('\nrank: ', end='')
            elif(self.isTd == 2): #address
                self.file.write(',\"address\":')
                # print('\taddress: ', end='')
            elif(self.isTd == 3): #amount
                self.file.write(',\"amount\":\"')
                # print('\tamount: ', end='')
            elif(self.isTd == 4): #percentage
                self.file.write(',\"percentage\":')
                # print('\tpercentage: ', end='')
        
            

    def handle_endtag(self, tag):
        if(tag == 'tbody'):
            self.inTbody = 0
        elif(tag == 'tr'):
            self.isTd = 0

    def handle_data(self, data):
        if(self.isTd == 2 and data.find('|') != -1): #address
            return

        if(self.isTd == 3 and len(data) > 0): #amount
            if(data.find('Ether') != -1):
                self.file.write(data[:-6] + '\"') #after .
                # print(data[:-6], end='')
            else:
                self.file.write(data.replace(',',''))
                # print(data.replace(',',''), end='') 

        elif(self.isTd > 0 and self.isTd < 5 and len(data.strip()) > 0):
            self.file.write('\"' + data + '\"')
            # print(data, end='')
        
        if(self.isTd == 4): #percentage
            self.file.write('},')
            

#global variable
starting_time = time.time()

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urllib.request.urlopen(req).read()
parser = wallet_info()

parser.feed(str(webpage))
parser.file.write('{\"timestamp\":\"' + str(int(time.time())) + '\"}]')

print("Ethereum.py DONE at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "\t Cost: " + str(time.time() - starting_time))
