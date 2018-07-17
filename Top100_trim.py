import json
import time

# load json file
with open('Top100.json') as file:
    top100 = json.load(file)

tem_list = list()
for coin in top100['data']:
    try:
        file = open('CoinData/' + coin['symbol'] +'.json')
        file.close()
        tem_list.append(coin)
    except:
        continue

top100['data'] = tem_list

with open("Top100_trim.json", "w") as write_file:
    json.dump(top100, write_file)
