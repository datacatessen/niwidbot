all: start

clean:
	rm -rf env

env:
	virtualenv env
	./env/bin/pip install -r requirements.txt

start: env
	./env/bin/python niwidbot.py

build:
	docker build -t niwidbot:latest .

run: build
	docker run niwidbot:latest

save: build
	docker save niwidbot:latest -o niwidbot.tar.gz
