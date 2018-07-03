import requests
import binance
from binance.client import Client
import urllib, time
from datetime import datetime

client = Client("gWCXQrWRYx15kqJsMagBgPHJaAn5yBgQncwlcm8rJGLQjjYlaXJ7GuoVfYmgB6dg",\
                "dgBC8P0TxTFbuUDHK1COklc57zGTqKqzRJOxqkX2bUJU5I2nnWStkAkJlUMjl89t")

def process_message(msg):
    # print("message type: {}".format(msg['e']))
    print('Trading Type: '+ msg['e'])
    print('the big E you want :' + str(msg['E']))
    print('the little s you want: ' + msg['s'])
    print('the little a you want ' + str(msg['a']))
    print('the price: ' + msg['p'])
    print('the qulity: ' + msg['q'])
    # print(msg['f'])
    # print(msg['l'])
    # print(msg['T'])
    # print(msg['m'])
    # print(msg['M'])
    print()

from binance.websockets import BinanceSocketManager
bm = BinanceSocketManager(client)
bm.start_aggtrade_socket('BTCUSDT', process_message)
bm.start()
#bm.close()
