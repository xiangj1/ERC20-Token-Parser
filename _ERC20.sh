#!/bin/sh

while true; do
	python3 EtherScanTop200.py
	mv token_symbol.json.new token_symbol.json
	rename -f 's/\.json.new$/\.json/' CoinData/*.new
done
