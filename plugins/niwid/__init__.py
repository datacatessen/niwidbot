import os
import random
import re

from lib.util import RateLimited
from plugins import EventHandler

img_path = 'imgs'
DOG_IMAGES = ['%s/%s' % (img_path, f) for f in os.listdir(img_path)
            if os.path.isfile(os.path.join(img_path, f))]

MENTION_REGEX = r'^<@(|[WU].+?)>(.*)'

class NiwidHandler(EventHandler):
    def __init__(self, slackclient, logger):
        EventHandler.__init__(self, slackclient, logger)
        self.user_id = self.client.api_call('auth.test')['user_id']
        self.logger.info("User ID is %s", self.user_id)

    @RateLimited(1)
    def niwid_response(self, channel):
        filename = random.choice(DOG_IMAGES)
        with open(filename, 'rb') as f:
            content = f.read()

        ext = os.path.splitext(filename)[1][1:]

        self.logger.info("Uploading %s with ext %s and %s bytes",
                    filename, ext, len(content))

        self.client.api_call(
            'files.upload',
            channels=channel,
            filetype=ext,
            file=content,
            title='NIWID'
        )

    def handle(self, event):
        if event['type'] == 'message' and 'subtype' not in event:
            matches = re.search(MENTION_REGEX, event['text'])
            if matches and matches.group(1) == self.user_id:
                self.niwid_response(event['channel'])
