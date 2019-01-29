FROM centos:7

COPY imgs imgs
COPY niwidbot.py niwidbot.py
COPY requirements.txt requirements.txt
COPY token.secret token.secret

RUN yum -y install epel-release
RUN yum -y install python-pip
RUN pip install -r requirements.txt

CMD python niwidbot.py
