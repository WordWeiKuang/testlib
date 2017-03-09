#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

' url handlers '

import re, time, json, logging, hashlib, base64, asyncio, os
from random import choice
import markdown2

from aiohttp import web

from coroweb import get, post
from apis import Page,APIError, APIValueError, APIResourceNotFoundError, APIPermissionError
from models import User, Info
from config import configs

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret

def check_user(request):
    if request.__user__ is None:
        raise APIPermissionError()

def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)

def text2html(text):
    lines = map(lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), filter(lambda s: s.strip() != '', text.split('\n')))
    return ''.join(lines)

@asyncio.coroutine
def cookie2user(cookie_str):
    '''
    Parse cookie and load user if cookie is valid.
    '''
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = yield from User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None

@get('/')
def index():
    return {
        '__template__': 'index.html'
    }

@get('/infos')
def base_html():
    return {
        '__template__': 'infos.html'
    }

@get('/infos')
def infos():
    return{
        '__template__':'infos.html'
    }

@get('/api/infos')
def api_infos(*, page='1'):
    page_index = get_page_index(page)
    num = yield from Info.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, infos=())
    infos = yield from Info.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, infos=infos)

@get('/api/info/{id}')
def api_get_info(*, id):
    info = yield from Info.find(id)
    return info

@post('/api/blogs/{id}')
def api_update_blog(id, request, *, name, summary, content):
    check_admin(request)
    blog = yield from Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    yield from blog.update()
    return blog

@post('/api/info')
def api_create_info(request, *, name, summary, content):
    pass

@post('/api/blogs/{id}')
def api_update_blog():
    pass

@get('/game/{flag}')
def game_finger_guess(flag):
    flag_list = ['rock','paper','scissors']
    retun_flag = choice(flag_list)
    if(flag==retun_flag):
        return dict(flag = retun_flag, ps = '握手言和')
    if(flag=='paper'and retun_flag=='scissors' or flag=='rock'and retun_flag=='paper' or flag=='scissors'and retun_flag=='rock'):
        return dict(flag = retun_flag, ps = '你输了')
    if(flag=='paper'and retun_flag=='rock' or flag=='rock'and retun_flag=='scissors' or flag=='scissors'and retun_flag=='paper'):
        return dict(flag=retun_flag, ps = '你赢了')
    if(flag != 'rock' and flag != 'paper' and flag != 'scissors'):
        return dict(flag=retun_flag, ps='不要乱搞')

