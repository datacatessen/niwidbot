import re
import requests
import urllib.parse

from lib.util import RateLimited
from plugins import EventHandler

RIGHTJIF_REGEX = r'^<@(|[WU].+?)>.*gif (.*)'

class RightJifHandler(EventHandler):
    def __init__(self, slackclient, logger):
        EventHandler.__init__(self, slackclient, logger)
        self.user_id = self.client.api_call('auth.test')['user_id']
        self.logger.info("[RightJif] User ID is %s", self.user_id)

    @RateLimited(1)
    def rightjif_response(self, channel, search_text):
        url = "http://192.168.4.3:8080/search/%s" % urllib.parse.quote_plus(search_text)
        response = requests.get(url)
        # TODO Error handling
        content = response.content
        self.logger.info("Got %s bytes from %s"% (len(content), url))

        self.client.api_call(
            'files.upload',
            channels=channel,
            filetype='gif',
            file=content,
            title=search_text
        )


    def handle(self, event):
        if event['type'] == 'message' and 'subtype' not in event:
            matches = re.match(RIGHTJIF_REGEX, event['text'])
            if matches and matches.group(1) == self.user_id:
                self.rightjif_response(event['channel'], matches.group(2))
