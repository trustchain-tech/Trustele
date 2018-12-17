import time

from io import BytesIO
from pyrogram import Client
from pyrogram.api.errors import FloodWait
from pyrogram.api.core import Long

from peewee import *

db = SqliteDatabase('aaa.sqlite')


# pyrogram signed to webogram unsigned
def access_hash_translate(access_hash: int):
    return str(Long.read(BytesIO(Long(access_hash)), signed=False))


def group_id_translate(group_id: int):
    return int(str(group_id)[4:])


class BaseModel(Model):
    class Meta:
        database = db


class ChatModel(BaseModel):
    id = IntegerField(primary_key=True)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    access_hash = CharField(null=True)


class TeleUser(ChatModel):
    phone_number = CharField(null=True)
    big_photo = BlobField(null=True)

    @classmethod
    def get_or_create(cls, user_from_tele):
        u = user_from_tele
        return super(TeleUser, cls).get_or_create(id=u.id,
            defaults={'username': u.username,
                      'first_name': u.first_name,
                      'last_name': u.last_name,
                      'access_hash': access_hash_translate(u.access_hash),
                      'phone_number': u.phone_number})


class TeleGroup(ChatModel):
    title = TextField(null=True)
    description = TextField(null=True)
    type = TextField(null=True)

    @classmethod
    def get_or_create(cls, group_from_tele):
        g = group_from_tele
        return super(TeleGroup, cls).get_or_create(id=group_id_translate(g.id),
            defaults={'username': g.username,
                      'first_name': g.first_name,
                      'last_name': g.last_name,
                      'access_hash': access_hash_translate(g.access_hash),
                      'title': g.title,
                      'description': g.description,
                      'type': g.type})


class Membership(BaseModel):
    user = ForeignKeyField(TeleUser, backref='membership')
    group = ForeignKeyField(TeleGroup, backref='membership')


class MyClient(Client):
    def __enter__(self):
        db.connect()
        if True:
            db.create_tables([TeleUser, TeleGroup, Membership])
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        db.close()


app = MyClient("+8615589910302",
             proxy=dict(
                 hostname="localhost",
                 port=1080,
             ),
             api_id=486772,
             api_hash='6c6ccc2cbc6673004b4f367f8a5f987b')




with app:
    my_groups = [d.chat for d in app.get_dialogs().dialogs if d.chat.type == 'group' or d.chat.type == 'supergroup']
    for g in my_groups:
        print("group : ", g.username)

        target = g.id  # Target channel/supergroup
        members = []  # List that will contain all the members of the target chat
        offset = 0  # Offset starts at 0
        limit = 200  # Amount of users to retrieve for each API call (max 200)

        while True:
            try:
                chunk = app.get_chat_members(target, offset)
            except FloodWait as e:  # Very large chats could trigger FloodWait
                time.sleep(e.x)  # When it happens, wait X seconds and try again
                continue

            if not chunk.chat_members:
                break  # No more members left

            members.extend(chunk.chat_members)
            offset += len(chunk.chat_members)
            print(offset, '..')
            break

        print('\n')

        with db.atomic():
            g.access_hash = app.resolve_peer(g.id).access_hash
            db_group, group_created = TeleGroup.get_or_create(g)
            for u in members:
                u.user.access_hash = app.resolve_peer(u.user.id).access_hash
                db_user, user_created = TeleUser.get_or_create(u.user)
                db_membership, mem_created = Membership.get_or_create(user=db_user, group=db_group)
                # path = app.download_media(u.user.photo.big_file_id, block=True)

# 'u' 'c' 's'
