from html.parser import HTMLParser
from urllib.request import Request, urlopen
import time

coin_name = ['bitcoin', 'bitcoin%20cash', 'litecoin', 'dash', 'bitcoin%20gold', 'dogecoin', 'reddcoin', 'vertcoin', 'peercoin', 'namecoin', 'feathercoin', 'blackcoin', 'auroacoin', 'novacoin']
coin_symbol = ['BTC', 'BCH', 'LTC', 'DASH', 'BTG', 'DOGE', 'RDD', 'VTC', 'PPC', 'NMC', 'FTC', 'BLK', 'AUR', 'NVC']

class wallet_info(HTMLParser):
    def __init__(self, symbol):
        HTMLParser.__init__(self)
        self.inTable = 0
        self.inTbody = 0
        self.rank = 0
        self.round = 2 # since we only want first two data that contains amount & percentage
        self.isData = 0
        self.isAddress = 0

        self.file = open('CoinData/' + symbol + '.json.top100', 'w+')
        self.file_str = '{\"data\":['

        # print('Symbol: ' + symbol)


        

    def handle_starttag(self, tag, attrs):
        # Only parse the data in table table-striped bb abtb
        if(tag == 'table'):
            for name, value in attrs:
                if(name =='class' and value == 'table table-striped bb abtb'):
                    self.inTable = 1
                    break
        
        # for daata in the table and starting with td
        elif(tag == 'td' and self.inTable == 1):
            for name, value in attrs:
                if(name == 'class' and value == 'hidden-phone'):
                    self.isData = 1
                elif(name == 'data-val' and self.isData == 1 and self.round > 0):
                    if(self.round == 2):
                        self.file_str += '\"amount\":\"%s\",'%value
                        # print('Amount: ' + value, end = '\t')
                    else:
                        self.file_str += '\"percentage\":\"' + value + '%\"},'
                        # print('Percentage: ' + value)

                    self.isData = 0
                    self.round -= 1
        
        elif(tag == 'tbody' and self.inTable == 1):
            self.inTbody = 1

        elif(tag == 'tr' and self.inTable == 1 and self.inTbody == 1):
            self.rank += 1
            self.file_str += '{\"rank\": \"%s\",'%self.rank
            # print(str(self.rank) + ', ', end=' ')

        elif(tag == 'a' and self.inTable == 1):
            for name, value in attrs:
                if(name == 'href' and value.find('https://bitinfocharts') != -1):
                    self.isAddress = 1
                    

        
    def handle_endtag(self, tag):
        # reset round for each address
        if(tag == 'tr'):
            self.round = 2

    def handle_data(self, data):
        if(self.isAddress == 1):
            self.file_str += '\"address\":\"%s\",'%data
            # print('Address: ' + data, end= '\t')
            self.isAddress = 0
        return
 
starting_time = time.time()

for i in range(0, len(coin_name)):
    url = 'https://bitinfocharts.com/top-100-richest-%s-addresses.html'%coin_name[i]
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    time.sleep(10)
    webpage = urlopen(req).read()
    parser = wallet_info(coin_symbol[i])
    parser.feed(str(webpage))
    parser.file.write(parser.file_str[:-1])
    parser.file.write('],\"timestamp\":\"' + str(int(time.time())) + '\"}')
    
# parser = wallet_info(coin_symbol[1])
# parser.feed(open('top-100-richest-bitcoin-addresses.html').read())


print("BitinfoCharts.py DONE at: " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + "\t Cost: " + str(time.time() - starting_time))