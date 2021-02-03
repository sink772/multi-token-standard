#
# Makefile
#

help:
	@./run.py -h

deploy:
	./run.py -e local deploy multi_token

deploy-gochain:
	./run.py -e gochain -k res/gochain.json deploy multi_token

deploy-bicon:
	./run.py -e bicon -k res/bicon.json deploy multi_token

deploy-gangnam:
	./run.py -e gangnam -k res/gangnam.json deploy multi_token

test:
	python -m unittest -v
