import time
from pyrogram import Client
from pyrogram.api.errors import FloodWait
from trustele.models.model import db
from trustele.models.model import TeleUser, TeleGroup, Membership


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

        with db.atomic():
            g.access_hash = app.resolve_peer(g.id).access_hash
            db_group, group_created = TeleGroup.get_or_create(g)
            for u in members:
                u.user.access_hash = app.resolve_peer(u.user.id).access_hash
                db_user, user_created = TeleUser.get_or_create(u.user)
                db_membership, mem_created = Membership.get_or_create(user=db_user, group=db_group)
                # path = app.download_media(u.user.photo.big_file_id, block=True)

# 'u' 'c' 's'
