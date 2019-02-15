from peewee import *
from pyrogram.api.core import Long
from io import BytesIO


db = SqliteDatabase('database.sqlite')

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


with db:
    for m in [TeleUser, TeleGroup, Membership]:
        if not db.table_exists(m):
            m.create_table(m)
