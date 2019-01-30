FROM python:2-alpine

COPY requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY imgs imgs

COPY niwidbot.py niwidbot.py
COPY token.secret token.secret

CMD python niwidbot.py
