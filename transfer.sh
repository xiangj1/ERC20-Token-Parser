#!/bin/sh

rsync -avP -e "ssh -i aliyun.pem" Coin/*.json root@120.78.154.6:/root/Coin/
rsync -avP -e "ssh -i aliyun.pem" Coin/*.txt root@120.78.154.6:/root/Coin/
rsync -avP -e "ssh -i aliyun.pem" Coin/CoinData/*.json root@120.78.154.6:/root/Coin/CoinData/