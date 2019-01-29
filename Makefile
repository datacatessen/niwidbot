env:
	virtualenv env
	./env/bin/pip install -r requirements.txt

start:
	./env/bin/python niwidbot.py
