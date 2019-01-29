#!/usr/bin/env python

import logging
import os
import time
import re
from slackclient import SlackClient

logging.basicConfig()

if 'SLACK_BOT_TOKEN' not in os.environ:
    raise ValueError("No SLACK_BOT_TOKEN in environment. export SLACK_BOT_TOKEN")

client = SlackClient(os.environ['SLACK_BOT_TOKEN'])

DOG_IMAGES = [

]
# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
MENTION_REGEX = r'^<@(|[WU].+?)>(.*)'

def parse_user_mention(slack_events):
    for event in slack_events:
        if event['type'] == 'message' and not 'subtype' in event:
            matches = re.search(MENTION_REGEX, event['text'])
            print matches
            if matches:
                return matches.group(1), matches.group(2).strip(), event['channel']
    return None, None, None

if __name__ == '__main__':
    if client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")

        # Read bot's user ID by calling Web API method `auth.test`
        id = client.api_call('auth.test')['user_id']
        while True:
            user_id, command, channel = parse_user_mention(client.rtm_read())
            print user_id, command, channel
            if user_id:
                print 'someone is talking to me!'
                # Sends the response back to the channel
                client.api_call(
                    'chat.postMessage',
                    channel=channel,
                    text=default_response
                )

            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")
