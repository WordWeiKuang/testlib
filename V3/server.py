# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, jsonify, request, make_response, redirect, g
from model import User, Paper, Item, Tag
from apis import Page, TestState, APIValueError, APIResourceNotFoundError
import json, uuid, re, hashlib
from datetime import datetime

__token__ = 'kwdev'

def get_mac_address():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return "-".join([mac[e:e+2] for e in range(0,11,2)])

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

def dict2obj(d):
    if isinstance(d, list):
        d = [dict2obj(x) for x in d]
    if not isinstance(d, dict):
        return d
    class C(object):
        pass
    o = C()
    for k in d:
        o.__dict__[k] = dict2obj(d[k])
    return o

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1  # disable caching
app.register_blueprint


@app.before_request
def user2ag():
    user = User.select()[0]
    if not user.user_agent or not user.mac_address and request.endpoint not in ('user2code', 'static'):
        return redirect(url_for('user2code'))
    tags = Tag.select()
    g.tags = tags

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route("/index")
def index():
    tags = Tag.select().paginate(0,1)
    tag = tags[0]
    papers = Paper.select().where(Paper.tag == tag)
    return render_template("papers.html", tag = tag, papers = papers)

_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
@app.route("/",methods=['Get','POST'])
def user2code():
    error = None
    user = User.select()[0]
    user_agent = request.headers.get('User-Agent')
    mac = get_mac_address()
    if user.mac_address == mac and user.user_agent == user_agent:
        return redirect(url_for('index'))
    if request.method == 'POST' :
        code = request.form['code']
        print(code)
        sha1 = hashlib.sha1()
        sha1.update(code.encode('utf-8'))
        if not code:# or not _RE_SHA1.match(code):
            error = '請輸入驗證碼'
        elif user.code != sha1.hexdigest():
            error = '驗證碼錯誤'
        else:
            mac = get_mac_address()
            user_agent = request.headers.get('User-Agent')
            user.mac_address = mac
            user.user_agent = user_agent
            user.save()
            return redirect(url_for('index'))
    return render_template("code.html", error = error)

@app.route("/test")
def test():
    return render_template("items.html")

@app.route("/error/<type>")
def error(type):
    error = ''
    if type == 'notfond':
        error = '暂无數據'
    return render_template("error.html", error = error, a ='qweqwe')

@app.route("/papers/<tag_id>")
def papers(tag_id):
    if not tag_id:
        tags = Tag.select().paginate(0,1)
    else:
        tags = Tag.select().where(Tag.id == tag_id)
    tag = tags[0]
    papers = Paper.select().where(Paper.tag == tag)
    return render_template("papers.html", tag = tag, papers = papers)

@app.route("/testing/<paper_id>/<index>")
def testing(paper_id, index='1'):
    index_index = get_page_index(index)
    num = Item.select().where(Item.paper == paper_id)
    if not num:
        error = '暂无题目'
        return render_template("error.html", error = error)
    p = Page(len(num), index_index, 1)
    items = Item.select().where((Item.paper == paper_id) & (Item.index == index))
    item = items[0]
    return render_template("items.html", item = item, page = p)

@app.route("/test/<paper_id>")
def testing2(paper_id):
    papers = Paper.select().where(Paper.id == paper_id)
    return render_template("item2.html", paper=papers[0])

@app.route("/test/results/<paper_id>")
def test_results(paper_id):
    if not paper_id:
        raise APIValueError('paper', 'not fond')
    return render_template("resultes.html", paper_id=paper_id)

@app.route("/update")
def client_update():
    return render_template("update.html")

@app.route("/api/results/<paper_id>")
def get_testResults(paper_id):
    d1 = datetime.now()
    if not paper_id:
        raise APIValueError('paper', 'not fond')
    paper = list(Paper.select().where(Paper.id == paper_id).dicts())[0]
    data = json.loads(paper['state'])
    print(paper['state'])
    res = data['results']
    paper['state'] = ''
    re_state = TestState(paper = paper)

    re_state.finish_items = list(Item.select().where(Item.id<<data['finish_items']).dicts())
    re_state.unfinish_items = list(Item.select().where(Item.id << data['unfinish_items']).dicts())
    re_state.true_items = list(Item.select().where(Item.id << data['true_items']).dicts())
    re_state.false_items = list(Item.select().where(Item.id << data['false_items']).dicts())
    '''
    items = list(Item.select().where(Item.paper==paper['id']).dicts())
    for item in items:
        for re in res:
            if item['id'] == re['item']:
                item['user_answer'] = re['user_answer']
        if item['id'] in data['finish_items']:
            re_state.finish_items.append(item)
        if item['id'] in data['unfinish_items']:
            re_state.unfinish_items.append(item)
        if item['id'] in data['true_items']:
            re_state.true_items.append(item)
        if item['id'] in data['false_items']:
            re_state.false_items.append(item)
    '''
    re_state.score = data['score']
    re_state.status = data['status']
    re_state.finish_time =data['finish_time']
    re_state.utime = data['utime']
    response = {'state': re_state.dicts()}
    d2 = datetime.now()
    return jsonify(response)

@app.route("/api/tags")
def get_tags():
    tags = Tag.select().dicts()
    response = {'tags': list(tags)}
    return jsonify(response)

@app.route("/api/papers/<tag_id>")
def get_papers(tag_id):
    if tag_id:
        tags = Tag.select().where(Tag.id == tag_id)
    else:
        tags = Tag.select().paginate(0,1)
    papers = Paper.select().where(Paper.tag << tags).dicts()#.paginate(0, 100)
    response = {'papers':list(papers)}
    return jsonify(response)

@app.route("/api/items/<paper_id>")
def get_items(paper_id):
    if not paper_id:
        raise  APIValueError('item', 'not fond')
    items = Item.select().where(Item.paper == paper_id).order_by(Item.index).dicts()
    response = {'items':items}
    return jsonify(response)

@app.route("/api/item/<paper_id>")
def get_item(paper_id):
    papers = Paper.select().where(Paper.id == paper_id).dicts()
    paper = list(papers)[0]
    paper['state'] = ''
    items = Item.select().where(Item.paper == paper_id).order_by(Item.index).dicts()
    state = TestState(paper=paper)
    response = {'state':state.dicts(),'items': list(items)}
    return jsonify(response)

@app.route("/api/testing/commit",methods=['POST'])
def commit_paper():
    data = request.json
    print(data)
    if not data:
        raise APIValueError('state', 'not fond')
    state = data.get('state')
    result_list = state.get('results', [])

    finish_items = state.get('finish_items', [])
    finappend = finish_items.append

    unfinish_items = state.get('unfinish_items', [])
    uappend = unfinish_items.append

    true_items = state.get('true_items', [])
    tappend = true_items.append

    false_items = state.get('false_items', [])
    print('len')
    print(len(false_items))
    falappend = false_items.append
    d1 = datetime.now()
    for i in result_list:
        item_id = i.get('item')
        item = Item.select().where(Item.id == item_id)[0]
        item.user_answer = i.get('user_answer')
        if item.user_answer:
            finappend(item.id)
        else:
            uappend(item.id)
        if item.user_answer == item.answer:
            state['score'] += item.score
            tappend(item.id)
        if item.user_answer and item.user_answer!=item.answer:
            falappend(item.id)
        item.save()
    d2 = datetime.now()
    state['status'] = '已完成'
    paper = state['paper']
    paper_id = paper.get('id')
    papers = Paper.select().where(Paper.id == paper_id)
    paper = papers[0]
    #state.pop('results')
    state.pop('paper')
    paper.state = json.dumps(state)
    paper.save()
    response = {'url': '/test/results/'+paper.id}
    return jsonify(response)

def run_server():
    app.run(host="127.0.0.1", port=23946, threaded=True)

if __name__ == "__main__":
    run_server()
