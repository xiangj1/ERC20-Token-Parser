import requests
import binance
from binance.client import Client
import urllib, time
from datetime import datetime
import time

client = Client("gWCXQrWRYx15kqJsMagBgPHJaAn5yBgQncwlcm8rJGLQjjYlaXJ7GuoVfYmgB6dg",\
                "dgBC8P0TxTFbuUDHK1COklc57zGTqKqzRJOxqkX2bUJU5I2nnWStkAkJlUMjl89t")

total_q = 0
current_time = 0

def process_message(msg):
    global current_time
    global total_q

    if(current_time == 0):
        current_time = int(str(msg['T'])[:-3])
        total_q += int(msg['q'])
        return
    

    data_time = int(str(msg['T'])[:-3])

    pass_second = data_time - current_time # if pass_second = 0 
    if(pass_second == 0):
        total_q += int(msg['q'])
    else:
        print("Current time: " + str(current_time)  + "\t Total Quality: " + str(total_q))
        total_q = 0

        for i in range(0, pass_second):
            total_q += 1
        current_time = data_time
        total_q += msg['q']

from binance.websockets import BinanceSocketManager
bm = BinanceSocketManager(client)
bm.start_aggtrade_socket('BTCUSDT', process_message)
bm.start()
#bm.close()
