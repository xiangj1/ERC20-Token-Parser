import requests
import binance
from binance.client import Client
import urllib, time
import datetime
import urllib.request as urllib2

client = Client("H5Zp4m7r1ng2Q4yqBPxKw94ZjBWwruO3NHhVYDZDUKCA6iok1XEZw4bct7K7vpxW",\
                "szM1wCzpyqXuuOTUdRLSxjCJn32JQwmDG8aDf4QiNKRGfqZZxSKwQkhnyk1SY3Eu")

REST_API_URL = ["https://api.powerbi.com/beta/547040db-1855-4320-9738-e6878f6271fc/datasets/\
ecb9d3e7-4778-4b3d-8c52-203de3c1eb8c/rows?key=yly7U8FcCD%2Bl%2FT6frVS4k3XbtsvBXqJ%2BO4kPfsqp%2Bf7s1F2TQYSvgGL%2BMWL87XgcdcmhpBoPJdbp%2Fp3zY9IgYQ%3D%3D"]

total_capital = [0]
total_amount = [0]
capital_per_second = [0]
current_time = [0]
tiny_amount = [0]
tiny_total = [0]
tiny_capital = [0]
tiny_capital_per =[0]
small_amount = [0]
small_total = [0]
small_capital = [0]
small_capital_per = [0]
medium_amount = [0]
medium_total = [0]
medium_capital_per = [0]
medium_capital = [0]
big_amount = [0]
big_total = [0]
big_capital = [0]
big_capital_per = [0]
large_amount = [0]
large_total = [0]
large_capital = [0]
large_capital_per = [0]
massive_amount = [0]
massive_total = [0]
massive_capital = [0]
massive_capital_per = [0]
super_amount = [0]
super_total = [0]
super_capital = [0]
super_capital_per = [0]

def process_message(msg):

    price = float(msg['p'])
    qty = float(msg['q'])
    size = qty
    
    
    if (str(msg['m']) =='True'):
        qty=-qty
    
    cap = price*qty
    capital_per_second[-1] += cap
    total_capital[-1] += cap
    total_amount[-1] += qty 
    
    if (current_time[-1] == 0):

        current_time[-1] = int(str(msg['T'])[:-3])

    else:

        data_time= int(str(msg['T'])[:-3])
        pass_second = int((data_time - current_time[-1])/2) # change time here

        if(pass_second >= 1):

            for i in range(0, pass_second):
                 
                if(i!= pass_second -1):

                    try:
                
                        # data that we're sending to Power BI REST API
                        data = '[{{"总资金净流入": "{0:0.2f}", "当下资金净流入": "{1:0.2f}","时间":"{2}",\
                        "当下微单买卖正负差":"{3:0.6f}","微单买卖正负差":"{4:0.6f}","微单资金净流入":"{5:0.2f}",\
                        "当下小单买卖正负差":"{6:0.6f}","小单买卖正负差":"{7:0.6f}","小单资金净流入":"{8:0.2f}",\
                        "当下中单买卖正负差":"{9:0.6f}","中单买卖正负差":"{10:0.6f}","中单资金净流入":"{11:0.2f}",\
                        "当下大单买卖正负差":"{12:0.6f}","大单买卖正负差":"{13:0.6f}","大单资金净流入":"{14:0.2f}",\
                        "当下特大单买卖正负差":"{15:0.6f}","特大单买卖正负差":"{16:0.6f}","特大单资金净流入":"{17:0.2f}",\
                        "当下超大买卖正负差":"{18:0.6f}","超大单买卖正负差":"{19:0.6f}","超大单资金净流入":"{20:0.2f}",\
                        "当下巨单买卖正负差":"{21:0.6f}","巨单买卖正负差":"{22:0.6f}","巨单资金净流入":"{23:0.2f}",\
                        "总买卖差":"{24:0.6f}","当下微单资金净流入":"{25:0.2f}","当下小单资金净流入":"{26:0.2f}","当下中单资金净流入":"{27:0.2f}",\
                        "当下大单资金净流入":"{28:0.2f}","当下特大单资金净流入":"{29:0.2f}","当下超大单资金净流入":"{30:0.2f}","当下巨单资金净流入":"{31:0.2f}"}}]'.\
                        format(total_capital[-1],capital_per_second[-1],str(datetime.datetime.fromtimestamp(current_time[-1]+1).strftime('%Y-%m-%d %H:%M:%S')),\
                        tiny_amount[-1],tiny_total[-1],tiny_capital[-1],small_amount[-1],small_total[-1],small_capital[-1],medium_amount[-1],medium_total[-1],medium_capital[-1],\
                        big_amount[-1],big_total[-1],big_capital[-1],large_amount[-1],large_total[-1],large_capital[-1],massive_amount[-1],massive_total[-1],massive_capital[-1],\
                        super_amount[-1],super_total[-1],super_capital[-1],total_amount[-1],tiny_capital_per[-1],small_capital_per[-1],medium_capital_per[-1],big_capital_per[-1],\
                        large_capital_per[-1],massive_capital_per[-1],super_capital_per[-1]).encode("utf-8")
                
                        # make HTTP POST request to Power BI REST API
                        req = urllib2.Request(REST_API_URL[-1], data)
                        response = urllib2.urlopen(req)
                        #print("POST request to Power BI with data:{0}".format(data))
                        #print("Response: HTTP {0} {1}\n".format(response.getcode(), response.read()))	
                
                        time.sleep(1)
                    except urllib2.HTTPError as e:
                        print("HTTP Error: {0} - {1}".format(e.code, e.reason))
                    except urllib2.URLError as e:
                        print("URL Error: {0}".format(e.reason))
                    except Exception as e:
                        print("General Exception: {0}".format(e))

                    #rewrite##
                    current_time[-1]=current_time[-1]+2 #cahnge the time here too for different update interval
                    capital_per_second[-1] = 0
                    tiny_amount[-1] = 0
                    tiny_capital_per[-1] = 0
                    small_amount[-1] = 0
                    small_capital_per[-1] = 0
                    medium_amount[-1] = 0
                    medium_capital_per[-1] = 0
                    big_amount[-1] = 0
                    big_capital_per[-1] =0
                    large_amount[-1] = 0
                    large_capital_per[-1] = 0
                    massive_amount[-1] = 0
                    massive_capital_per[-1] = 0
                    super_amount[-1] = 0
                    massive_capital_per[-1] = 0
    
    ########DO#######
    if (size<= 0.001):                               #need to figure out how to choose order size for different tokens
        tiny_amount[-1] += qty
        tiny_total[-1] += qty
        tiny_capital[-1] += cap
        tiny_capital_per[-1] += cap
    elif(size > 0.001 and size<=0.01):
        small_amount[-1] += qty
        small_total[-1] += qty
        small_capital[-1] += cap
        small_capital_per[-1] += cap
    elif(size>0.01 and size<= 0.1):
        medium_amount[-1] += qty
        medium_total[-1] += qty
        medium_capital[-1] += cap
        medium_capital_per[-1] += cap
    elif(size>0.1 and size <=1):
        big_amount[-1] += qty
        big_total[-1] += qty
        big_capital[-1] += cap
        big_capital_per[-1] += cap
    elif(size >1 and size <=10):
        large_amount[-1] += qty
        large_total[-1] += qty
        large_capital[-1] += cap
        large_capital_per[-1] += cap
    elif(size >10 and size <= 100):
        massive_amount[-1] += qty
        massive_total[-1] += qty
        massive_capital[-1] += cap
        massive_capital_per[-1] += cap
    else:
        super_amount[-1] +=qty
        super_total[-1] += qty
        super_capital[-1] += cap
        super_capital_per[-1] += cap

#websocket
from binance.websockets import BinanceSocketManager
bm = BinanceSocketManager(client)
bm.start_aggtrade_socket('BTCUSDT', process_message)
bm.start()
#bm.close()                    
                    

                    

        
