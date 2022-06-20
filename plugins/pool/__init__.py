import os
import re
import requests

from bs4 import BeautifulSoup
from lib.util import RateLimited
from plugins import EventHandler
from tabulate import tabulate

POOL_REGEX = r'^<@(|[WU].+?)>(.*pools?.*)'

class PoolHandler(EventHandler):
    def __init__(self, slackclient, logger):
        EventHandler.__init__(self, slackclient, logger)
        self.user_id = self.client.api_call('auth.test')['user_id']
        self.logger.info("[PoolHandler] User ID is %s", self.user_id)

    @RateLimited(1)
    def pool_response(self, channel):
        message = "```\n" + tabulate(self.get_pool_status(), headers='firstrow', tablefmt='fancy_grid') + "\n```"
        print(message)
        self.logger.info("[PoolHandler] Sending status to %s" % channel)
        response = self.client.api_call(
            "chat.postMessage", channel=channel, text=message
        )

        if not response["ok"]:
            self.logger.error(
                "Error from chat.postMessage\n%s" % json.dumps(response, indent=2)
            )

    def handle(self, event):
        if event['type'] == 'message' and 'subtype' not in event:
            matches = re.match(POOL_REGEX, event['text'])
            if matches and matches.group(1) == self.user_id:
                self.pool_response(event['channel'])

    def get_pool_status(self):
        response = requests.get("https://www.columbiaassociation.org/facilities/indoor-swimming-pools/pool-locations/status/")
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find("table", id="tablepress-1")
        # print(table.prettify())
        body = table.find("tbody")
        rows = body.findAll('tr')
        l = list()
        for row in rows:
            cells = row.find_all("td")
            name = cells[0].get_text()
            count = int(cells[1].get_text()) if cells[1].get_text() else None
            status = cells[2].get_text()
            l.append((name, count, status))
        l.sort(key = lambda x: (x[1] is None, x[1]))
        return [("Pool Name", "Count", "Status")] + l
