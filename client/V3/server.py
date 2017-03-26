# -*- coding: utf-8 -*-
from flask import Flask, url_for, render_template, jsonify, request, make_response
from model import User, Paper, Item, Tag

app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 1  # disable caching


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route("/")
def landing():
    return render_template("papers.html")

@app.route("/item")
def item():
    return render_template("item.html")

@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/api/tags")
def get_tags():
    tags = Tag.select().dicts()
    response = {'tags': list(tags)}
    return jsonify(response)

@app.route("/api/papers")
def get_papers():
    papers = Paper.select().dicts()#.paginate(0, 100)
    response = {'papers':list(papers)}
    return jsonify(response)

def run_server():
    app.run(host="127.0.0.1", port=23948, threaded=True)


if __name__ == "__main__":
    run_server()
