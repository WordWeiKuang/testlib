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
from models import User, Tag, Paper, Item
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
def index(request):
    return {
        '__template__': 'index.html'
    }

@get('/manage/')
def manage_index():
    return {
        '__template__': 'manage_index.html'
    }

@get('/manage/tags')
def manage_tag(*, page='1'):
    return {
        '__template__': 'manage_tag.html',
        'page_index': get_page_index(page)
    }

@get('/manage/tag/create')
def manage_create_tag():
    return {
        '__template__': 'manage_tag_edit.html',
        'id': '',
        'action': '/api/tag'
    }


@get('/manage/tags/edit')
def manage_edit_tag(*, id):
    return {
        '__template__': 'manage_tag_edit.html',
        'id': id,
        'action': '/api/tag/%s' % id
    }

@get('/manage/papers')
def manage_papers(*, page='1'):
    return {
        '__template__': 'manage_papers.html',
        'page_index': get_page_index(page)
    }

@get('/manage/paper/create')
def manage_paper_tag():
    return {
        '__template__': 'manage_paper_edit.html',
        'id': '',
        'action': '/api/paper'
    }

@get('/manage/paper/edit')
def manage_edit_paper(*, id):
    return {
        '__template__': 'manage_paper_edit.html',
        'id': id,
        'action': '/api/paper/%s' % id
    }

@get('/manage/items')
def manage_items(*, page='1', paper_id=''):
    return {
        '__template__': 'manage_items.html',
        'page_index': get_page_index(page),
        'paper_id': paper_id
    }

@get('/manage/item/create')
def manage_item_create(*, paper_id=''):
    return {
        '__template__': 'manage_item_edit.html',
        'id': '',
        'action': '/api/item',
        'paper_id': paper_id
    }

@get('/manage/item/edit')
def manage_edit_item(*, id):
    return {
        '__template__': 'manage_item_edit.html',
        'id': id,
        'action': '/api/item/%s' % id
    }

#api

@get('/signin')
def signin():
    return {
        '__template__': 'signin.html'
    }


@post('/api/authenticate')
def authenticate(*, name, passwd):
    if not name:
        raise APIValueError('name', 'Invalid name.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = yield from User.findAll('name=?', [name])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]
    # check passwd:
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')
    # authenticate ok, set cookie:
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r

@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r

@get('/api/tags')
def api_tags(request, *, page='1'):
    check_admin(request)
    page_index = get_page_index(page)
    num = yield from Tag.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, tags=())
    tags = yield from Tag.findAll(orderBy='ctime desc', limit=(p.offset, p.limit))
    return dict(page=p, tags=tags)

#tag
#get tags no page
@get('/api/get_tags')
def api_get_tags(request):
    check_admin(request)
    num = yield from Tag.findNumber('count(id)')
    if num == 0:
        return []
    tags = yield from Tag.findAll(orderBy='ctime desc')
    return dict(tags=tags)

#return a tag by tag_id
@get('/api/tag/{id}')
def api_get_tag(*, id):
    tag = yield from Tag.find(id)
    return tag

#create tag
@post('/api/tag')
def api_create_tag(request, *, name, brief):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    tag = Tag(name=name.strip(), brief=brief.strip())
    yield from tag.save()
    return tag

#edit tag
@post('/api/tag/{id}')
def api_update_tag(id, request, *, name, brief):
    check_admin(request)
    tag = yield from Tag.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    tag.name = name.strip()
    tag.brief = brief.strip()
    yield from tag.update()
    return tag

#delete tag
@post('/api/tags/{id}/delete')
def api_delete_tag(request, *, id):
    check_admin(request)
    tag = yield from Tag.find(id)
    yield from tag.remove()
    return dict(id=id)

#paper
#create paper
@post('/api/paper')
def api_create_paper(request, *, name, brief, tag):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not tag or not tag.strip():
        raise APIValueError('tag', 'tag cannot be empty.')
    paper = Paper(name=name.strip(), brief=brief.strip(), tag=tag.strip(), munber=0, total=0)
    yield from paper.save()
    return paper

#return a paper by id
@get('/api/paper/{id}')
def api_get_paper(*, id):
    paper = yield from Paper.find(id)
    return paper

#get papers no page
@get('/api/get_papers')
def api_get_papers(request):
    check_admin(request)
    num = yield from Paper.findNumber('count(id)')
    if num == 0:
        return []
    papers = yield from Paper.findAll(orderBy='ctime desc')
    return dict(papers=papers)

@get('/api/papers')
def api_papers(request, *, page='1'):
    check_admin(request)
    page_index = get_page_index(page)
    num = yield from Paper.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, papers=())
    papers = yield from Paper.findAll(orderBy='ctime desc', limit=(p.offset, p.limit))
    for item in papers:
        tag = yield from Tag.find(item.tag)
        item.tag = tag.name
    return dict(page=p, papers=papers)

#edit paper
@post('/api/paper/{id}')
def api_update_paper(id, request, *, name, brief, tag):
    check_admin(request)
    paper = yield from Paper.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not tag or not tag.strip():
        raise APIValueError('tag', 'tag cannot be empty.')
    paper.name = name.strip()
    paper.brief = brief.strip()
    paper.tag = tag.strip()
    yield from paper.update()
    return paper

#delete paper
@post('/api/paper/{id}/delete')
def api_delete_paper(request, *, id):
    check_admin(request)
    paper = yield from Paper.find(id)
    yield from paper.remove()
    return dict(id=id)

#item
'''
item list

page:str
id:str paperId

'''
@get('/api/items/{id}')
def api_items(request, *, page='1', id):
    check_admin(request)
    page_index = get_page_index(page)
    num = yield from Item.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, items=())
    items = yield from Item.findAll('paper=?', [id], orderBy='ctime desc', limit=(p.offset, p.limit))
    return dict(page=p, items=items)

#create item
@post('/api/item')
def api_create_item(request, *, content, answer, answer_type, paper_id, **kwargs):
    check_admin(request)
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    if not answer or not answer.strip():
        raise APIValueError('answer', 'answer cannot be empty.')
    if not answer_type or not answer_type.strip():
        raise APIValueError('answer_type', 'answer_type cannot be empty.')
    if not paper_id or not paper_id.strip():
        raise APIValueError('paper_id', 'paper_id cannot be empty.')
    paper = yield from Paper.find(paper_id)
    item = Item(index=paper.munber, paper=paper.id, content=content.strip(), answer=answer.strip(), answer_type=answer_type.strip())
    if (answer_type.strip()=='选择题'):
        answer_A = kwargs.get('answer_A', None)
        answer_B = kwargs.get('answer_B', None)
        answer_C = kwargs.get('answer_C', None)
        answer_D = kwargs.get('answer_D', None)
        item.answer_A = answer_A.strip()
        item.answer_B = answer_B.strip()
        item.answer_C = answer_C.strip()
        item.answer_D = answer_D.strip()
    yield from item.save()
    paper.munber +=1
    yield from paper.update()
    return item

#return a item
@get('/api/item/{id}')
def api_get_item(*, id):
    item = yield from Item.find(id)
    return item

#edit item
@post('/api/item/{id}')
def api_update_item(id, request, *, content, answer, answer_type, paper_id, **kwargs):
    check_admin(request)
    item = yield from Item.find(id)
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    if not answer or not answer.strip():
        raise APIValueError('answer', 'answer cannot be empty.')
    if not answer_type or not answer_type.strip():
        raise APIValueError('answer_type', 'answer_type cannot be empty.')
    if not paper_id or not paper_id.strip():
        raise APIValueError('paper_id', 'paper_id cannot be empty.')
    item.content = content.strip()
    item.answer = answer.strip()
    item.answer_type = answer_type.strip()
    item.paper = paper_id.strip()
    if (answer_type.strip()=='选择题'):
        answer_A = kwargs.get('answer_A', None)
        answer_B = kwargs.get('answer_B', None)
        answer_C = kwargs.get('answer_C', None)
        answer_D = kwargs.get('answer_D', None)
        item.answer_A = answer_A.strip()
        item.answer_B = answer_B.strip()
        item.answer_C = answer_C.strip()
        item.answer_D = answer_D.strip()
    yield from item.update()
    return item

#delete item
@post('/api/item/{id}/delete')
def api_delete_item(request, *, id):
    check_admin(request)
    item = yield from Item.find(id)
    yield from item.remove()
    return dict(id=id)


"""
update client data API

"""

#get update
@get('/api/update')
def client_update_data():
    tags = yield from Tag.findAll()
    papers = yield from Paper.findAll()
    items = yield from Item.findAll()
    return dict(tags = tags, papers = papers, items = items)