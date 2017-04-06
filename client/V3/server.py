# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, jsonify, request, make_response
from model import User, Paper, Item, Tag
from apis import Page, TestState, APIValueError, APIResourceNotFoundError
import json

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1  # disable caching

def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p

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

@app.route("/api/item/<paper_id>")
def get_item(paper_id):
    num = Item.select().where(Item.paper == paper_id)
    if not num:
        raise APIValueError('item')
    papers = Paper.select().where(Paper.id == paper_id).dicts()
    paper = list(papers)[0]
    items = Item.select().where(Item.paper == paper_id).order_by(Item.index).dicts()
    state = TestState(paper=paper, items=list(items))
    response = {'state':state.dicts()}
    return jsonify(response)

def run_server():
    app.run(host="127.0.0.1", port=23948, threaded=True)


if __name__ == "__main__":
    run_server()
