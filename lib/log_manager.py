import logging


class Log():
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(level = logging.DEBUG)
        self.handler = logging.FileHandler("../log.txt")
        self.handler.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.console = logging.StreamHandler()
        self.console.setFormatter(self.formatter)
        self.console.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)
        self.logger.addHandler(self.console)
