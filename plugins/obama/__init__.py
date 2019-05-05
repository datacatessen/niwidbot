import os
import re

from lib.util import RateLimited
from plugins import EventHandler

with open('imgs/obama.png', 'rb') as f:
    OBAMA = f.read()

OBAMA_REGEX = r'^<@(|[WU].+?)>(.*[Oo]bama.*)'

class ObamaHandler(EventHandler):
    def __init__(self, slackclient, logger):
        EventHandler.__init__(self, slackclient, logger)
        self.user_id = self.client.api_call('auth.test')['user_id']
        self.logger.info("[ObamaHandler] User ID is %s", self.user_id)

    @RateLimited(1)
    def obama_response(self, channel):
        self.logger.info("[ObamaHandler] Uploading Obama with %s bytes", len(OBAMA))
        self.client.api_call(
            'files.upload',
            channels=channel,
            filetype='png',
            file=OBAMA,
            title='Upvoting Obama'
        )

    def handle(self, event):
        if event['type'] == 'message' and 'subtype' not in event:
            matches = re.match(OBAMA_REGEX, event['text'])
            if matches and matches.group(1) == self.user_id:
                self.obama_response(event['channel'])
