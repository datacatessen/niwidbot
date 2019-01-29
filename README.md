# niwidbot

Posts No Idea What I'm Doing dogs to a Slack channel when it is mentioned `@NIWIDBot`

## Install

Create a file called `token.secret` which contains the Slack token that can be used the client.

To run locally:
```
make start
```

To build and run as Docker:

```
sudo docker build -t niwidbot:latest .
sudo docker run niwidbot:latest
```
