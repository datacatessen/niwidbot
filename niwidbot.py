#!/usr/bin/env python

import logging
import os
import sys
import time

from pyee import EventEmitter
from slackclient import SlackClient

from lib.util import getPluginsByType

logging.basicConfig(level=logging.INFO, format='%(asctime)-15s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if 'SLACK_CLIENT_TOKEN' not in os.environ:
    logger.error("No SLACK_CLIENT_TOKEN set in environment")
    sys.exit(1)

client = SlackClient(os.environ['SLACK_CLIENT_TOKEN'])
ee = EventEmitter()

PLUGIN_FOLDER = "./plugins"
RTM_READ_DELAY_MS = 5

def init_plugins():
    for cls in getPluginsByType(PLUGIN_FOLDER, 'EventHandler'):
        logger.info("Loading plugin: %s" % cls.__name__)
        handler = cls(client, logger)
        ee.on('slack.events', handler.handle)

if __name__ == '__main__':
    logger.info("Starting bot...")
    init_plugins()

    if client.rtm_connect(with_team_state=False):
        # Read bot's user ID by calling Web API method `auth.test`
        bot_user_info = client.api_call(
            'users.info', user=client.api_call('auth.test')['user_id'])
        logger.info("Bot '%s' connected and running!" %
                    (bot_user_info['user']['profile']['real_name_normalized']))

        while True:
            for event in client.rtm_read():
                ee.emit('slack.events', event)
            time.sleep(RTM_READ_DELAY_MS / 1000.0)
    else:
        logging.error("Connection failed")
