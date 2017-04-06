import time, uuid
from peewee import SqliteDatabase, Model, TextField, DoubleField, IntegerField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

db = SqliteDatabase('./peewee.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = TextField(primary_key=True,default=next_id)
    name = TextField()
    email = TextField()
    image = TextField(null=True)
    code = TextField()
    setting = TextField()
    tag = TextField()
    ctime = DoubleField(default=time.time)

class Tag(BaseModel):
    id = TextField(primary_key=True,default=next_id)
    pid = TextField(null=True)
    name = TextField()
    brief = TextField()
    cover = TextField(null=True)
    ctime = DoubleField(default=time.time)

class Paper(BaseModel):
    id = TextField(primary_key=True,default=next_id)
    name = TextField()
    tag = TextField(null=True)
    cover = TextField(null=True)
    munber = IntegerField(null=True)
    total = IntegerField(null=True)
    finish_time = DoubleField(null=True)
    ctime = DoubleField(default=time.time)

class Item(BaseModel):
    id = TextField(primary_key=True,default=next_id)
    index = IntegerField()
    content = TextField()
    answer = TextField()
    answer_list = TextField()
    answer_type = TextField()
    user_answer = TextField()
    score = IntegerField(null=True)
    paper = TextField()
    ctime = DoubleField(default=time.time)

