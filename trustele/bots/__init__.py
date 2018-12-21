
class Bot(object):
    def __init__(self, account):
        self.phone = account
        self.sender = None
        self.fetcher = None

    def login(self):
        pass

    def logout(self):
        pass

    def validate(self, valid_code):
        pass
