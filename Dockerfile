FROM python:3.7-alpine

COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY imgs imgs

COPY lib lib
COPY plugins plugins
COPY niwidbot.py niwidbot.py
COPY token.secret token.secret

CMD python niwidbot.py
