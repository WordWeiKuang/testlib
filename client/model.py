from peewee import *

import time, uuid

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    id = TextField(primary_key=True,default=next_id)
    name = TextField()
    passwd = TextField()
    email = TextField()
    image = TextField(null=True)
    code = TextField()
    ctime = DoubleField(default=time.time)

class Paper(Model):
    id = TextField(primary_key=True,default=next_id)
    name = TextField()
    tag = TextField(null=True)
    munber = IntegerField(null=True)
    total = IntegerField(null=True)
    ctime = DoubleField(default=time.time)

class Item(Model):
    id = TextField(primary_key=True,default=next_id)
    index = IntegerField()
    content = TextField()
    answer = TextField()
    answer_list = TextField()
    answer_type = TextField()
    score = IntegerField(null=True)
    paper = TextField()
    ctime = DoubleField(default=time.time)

'''
db = SqliteDatabase('data.db')
db.connect()
db.create_tables([User,Paper,Item])

user = User.create(name='charlie', passwd='1111', email='1111@test.com')
user.save()

paper = Paper.create(name='电工测试题',tag='深圳技师学院特种测试题',munber=100,total = 100)
paper.save()

item = Item.create(index=1,content='将一根导线均匀拉长为原长的2倍，则它的阻值为原阻值的(   )倍。',
                   answer_list='A.1    B．2    C．4',answer_type='choice',answer='c',score=1,
                   paper='')
item.save()

'''

