all: start

clean:
	rm -rf env

env:
	virtualenv env
	./env/bin/pip install pip-tools
	./env/bin/pip-compile --output-file requirements.txt requirements.in
	./env/bin/pip install -r requirements.txt

start: env
	./env/bin/python niwidbot.py

build:
	docker build -t niwidbot:latest .

run: build
	docker run -e SLACK_CLIENT_TOKEN=${SLACK_CLIENT_TOKEN} niwidbot:latest

save: build
	docker save niwidbot:latest -o niwidbot.tar.gz
