#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Models for user, blog, comment.
'''

__author__ = 'Michael Liao'

import time, uuid

from orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

class User(Model):
    __table__ = 'user'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    passwd = StringField(ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    cover = TextField()
    code_key = TextField()
    code_sha = TextField()
    admin = BooleanField()
    tag = TextField()
    update_time = FloatField(default=time.time)
    ctime = FloatField(default=time.time)

class Tag(Model):
    __table__ = 'tag'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    pid = StringField(ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    brief = TextField()
    cover = TextField()
    update_time = FloatField(default=time.time)
    ctime = FloatField(default=time.time)

class Paper(Model):
    __table__ = 'paper'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    tag = StringField(ddl='varchar(50)')
    cover = TextField()
    brief = TextField()
    munber = IntegerField()
    total = FloatField()
    update_time = FloatField(default=time.time)
    ctime = FloatField(default=time.time)

class Item(Model):
    __table__ = 'item'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    index = IntegerField()
    content = TextField()
    answer = TextField()
    answer_list = TextField()
    answer_A = TextField()
    answer_B = TextField()
    answer_C = TextField()
    answer_D = TextField()
    #TOF/MCQ
    answer_type = StringField(ddl='varchar(255)')
    score = IntegerField(default=1)
    paper = StringField(ddl='varchar(50)')
    update_time = FloatField(default=time.time)
    ctime = FloatField(default=time.time)