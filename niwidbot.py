#!/usr/bin/env python

import logging
import os
import time
import random
import re

from slackclient import SlackClient

if 'SLACK_BOT_TOKEN' not in os.environ:
    raise ValueError("No SLACK_BOT_TOKEN in environment. export SLACK_BOT_TOKEN")

logging.basicConfig(level=logging.INFO,format='%(asctime)-15s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

client = SlackClient(os.environ['SLACK_BOT_TOKEN'])

img_path = 'imgs'
DOG_IMAGES = [ '%s/%s' % (img_path, f) for f in os.listdir(img_path) if os.path.isfile(os.path.join(img_path, f)) ]

# constants
RTM_READ_DELAY_MS = 100
MENTION_REGEX = r'^<@(|[WU].+?)>(.*)'

def parse_user_mention(slack_events):
    for event in slack_events:
        if event['type'] == 'message' and not 'subtype' in event:
            matches = re.search(MENTION_REGEX, event['text'])
            if matches:
                return matches.group(1), matches.group(2).strip(), event['channel']
    return None, None, None

if __name__ == '__main__':
    if client.rtm_connect(with_team_state=False):
        logger.info("NIWIDBot connected and running!")

        # Read bot's user ID by calling Web API method `auth.test`
        id = client.api_call('auth.test')['user_id']
        while True:
            user_id, command, channel = parse_user_mention(client.rtm_read())
            if user_id:
                filename = random.choice(DOG_IMAGES)
                with open(filename, 'rb') as f:
                    content = f.read()

                ext = os.path.splitext(filename)[1][1:]

                logger.info("Uploading %s with ext %s and %s bytes", filename, ext, len(content))

                client.api_call(
                    'files.upload',
                    channels=channel,
                    filetype=ext,
                    file=content,
                    title='NIWID'
                )

            time.sleep(RTM_READ_DELAY_MS / 1000.0)
    else:
        logging.error("Connection failed")
