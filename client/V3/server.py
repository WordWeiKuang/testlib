# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, jsonify, request, make_response
from model import User, Paper, Item, Tag
from apis import Page, TestState, APIValueError, APIResourceNotFoundError
import json
from datetime import datetime

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


#@app.before_request
#def testing2state():
#    pass

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route("/")
def landing():
    tags = Tag.select().paginate(0, 1)
    tag = tags[0]
    return render_template("papers.html", tag = tag)

@app.route("/test")
def index():
    return render_template("items.html")

@app.route("/papers/<tag_id>")
def papers(tag_id):
    if not tag_id:
        tags = Tag.select().paginate(0,1)
    else:
        tags = Tag.select().where(Tag.id == tag_id)
    tag = tags[0]
    return render_template("papers.html", tag = tag)

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

@app.route("/api/results/<paper_id>")
def get_testResults(paper_id):
    d1 = datetime.now()
    if not paper_id:
        raise APIValueError('paper', 'not fond')
    paper = list(Paper.select().where(Paper.id == paper_id).dicts())[0]
    data = json.loads(paper['state'])
    paper['state'] = ''
    re_state = TestState(paper = paper)
    re_state.finish_items = list(Item.select().where(Item.id<<data['finish_items']).dicts())
    re_state.unfinish_items = list(Item.select().where(Item.id << data['unfinish_items']).dicts())
    re_state.true_items = list(Item.select().where(Item.id << data['true_items']).dicts())
    re_state.false_items = list(Item.select().where(Item.id << data['false_items']).dicts())

    re_state.score = data['score']
    re_state.status = data['status']
    re_state.finish_time =data['finish_time']
    re_state.utime = data['utime']
    response = {'state': re_state.dicts()}
    d2 = datetime.now()
    print(d2-d1)
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
    num = Item.select().where(Item.paper == paper_id)
    if not num:
        raise APIValueError('item')
    papers = Paper.select().where(Paper.id == paper_id).dicts()
    paper = list(papers)[0]
    items = Item.select().where(Item.paper == paper_id).order_by(Item.index).dicts()
    state = TestState(paper=paper)
    response = {'state':state.dicts(),'items': list(items)}
    return jsonify(response)

@app.route("/api/testing/commit",methods=['POST'])
def commit_paper():
    data = request.json
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
    falappend = false_items.append
    for i in result_list:
        item_id = i.get('item')
        items = Item.select().where(Item.id == item_id)
        item = items[0]
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
    state['status'] = '已完成'
    paper = state['paper']
    paper_id = paper.get('id')
    papers = Paper.select().where(Paper.id == paper_id)
    paper = papers[0]
    state.pop('results')
    state.pop('paper')
    paper.state = json.dumps(state)
    paper.save()
    response = {'url': '/test/results/'+paper.id}
    return jsonify(response)

def run_server():
    app.run(host="127.0.0.1", port=23948, threaded=True)

if __name__ == "__main__":
    run_server()
