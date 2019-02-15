from pyrogram import Client
from trustele.models.model import db

API_ID = 486772
API_HASH = '6c6ccc2cbc6673004b4f367f8a5f987b'
PROXY = dict(hostname="localhost", port=1080)


class Bot(object):
    app = None
    phone = None
    db = db

    @classmethod
    def login(cls, account, phone_callback):
        cls.phone = account
        try:
            db.connect()
            cls.app = Client(cls.phone, proxy=PROXY,
                             api_id=API_ID, api_hash=API_HASH,
                             phone_number=cls.phone, phone_code=phone_callback)
            cls.app.start()
        except Exception as e:
            raise

    @classmethod
    def logout(cls):
        cls.app.stop()
        db.close()
        cls.phone = None
