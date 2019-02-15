import time
from pyrogram.api.errors import FloodWait
from trustele.models.model import TeleUser, TeleGroup, Membership
from trustele.bots import Bot


class Fetcher(Bot):
    def fetch(self):
        my_groups = [d.chat for d in self.app.get_dialogs().dialogs if d.chat.type == 'group' or d.chat.type == 'supergroup']
        for g in my_groups:

            target = g.id  # Target channel/supergroup
            members = []  # List that will contain all the members of the target chat
            offset = 0  # Offset starts at 0
            limit = 200  # Amount of users to retrieve for each API call (max 200)

            while True:
                try:
                    chunk = self.app.get_chat_members(target, offset)
                except FloodWait as e:  # Very large chats could trigger FloodWait
                    time.sleep(e.x)  # When it happens, wait X seconds and try again
                    continue

                if not chunk.chat_members:
                    break  # No more members left

                members.extend(chunk.chat_members)
                offset += len(chunk.chat_members)

            with self.db.atomic():
                g.access_hash = self.app.resolve_peer(g.id).access_hash
                db_group, group_created = TeleGroup.get_or_create(g)
                for u in members:
                    u.user.access_hash = self.app.resolve_peer(u.user.id).access_hash
                    db_user, user_created = TeleUser.get_or_create(u.user)
                    db_membership, mem_created = Membership.get_or_create(user=db_user, group=db_group)
                    # path = app.download_media(u.user.photo.big_file_id, block=True)

# 'u' 'c' 's'
