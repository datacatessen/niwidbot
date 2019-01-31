class EventHandler():

    def __init__(self, slackclient, logger):
        self.client = slackclient
        self.logger = logger

    def handle(self, event):
        raise NotImplementedError('Method not implemented')
