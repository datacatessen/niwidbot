import json
import os
import re

import requests

from lib.util import RateLimited
from plugins import EventHandler

GRLC_REGEX = r"^<@(|[WU].+?)>(.*grlc.*)"
ENDPOINT = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=2475"

headers = {
    "X-CMC_PRO_API_KEY": "78d79599-642b-4649-835a-f2e7ac55fa8e",
    "Accept": "application/json",
}


class GrlcHandler(EventHandler):
    def __init__(self, slackclient, logger):
        EventHandler.__init__(self, slackclient, logger)
        self.user_id = self.client.api_call("auth.test")["user_id"]
        self.logger.info("[GrlcHandler] User ID is %s", self.user_id)

    def get_price(self):
        re = requests.get(ENDPOINT, headers=headers)
        re.raise_for_status()
        return re.json()["data"]["2475"]["quote"]["USD"]["price"]

    @RateLimited(1)
    def grlc_response(self, channel):
        price = self.get_price()
        message = "Current GRLC Price: $%s" % price
        self.logger.info("[GrlcHandler] %s to %s" % (message, channel))
        response = self.client.api_call(
            "chat.postMessage", channel=channel, text=message
        )

        if not response["ok"]:
            self.logger.error(
                "Error from chat.postMessage\n%s" % json.dumps(response, indent=2)
            )

    def handle(self, event):
        if event["type"] == "message" and "subtype" not in event:
            matches = re.match(GRLC_REGEX, event["text"], re.IGNORECASE)
            if matches and matches.group(1) == self.user_id:
                self.grlc_response(event["channel"])
