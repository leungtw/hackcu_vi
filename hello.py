# from flask import Flask, render_template, redirect, flash, request
from pymongo import MongoClient
from pprint import pprint
import datetime
import requests
import json
pw = "Redrider3%21"
client = MongoClient('''mongodb://sale3054:Redrider3%21@cluster0-shard-00-00-g3da1.mongodb.net:27017,cluster0-shard-00-01-g3da1.mongodb.net:27017,cluster0-shard-00-02-g3da1.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority''')
db = client.test_database

post = {"author" : "Mike", "text" : "My first blog post!", "tags" : ["element1", "element2"],
"date": datetime.datetime.utcnow()}
posts = db.posts
post_id = posts.insert_one(post).inserted_id
pprint(post_id)

pprint(db.list_collection_names())



# serverStatusResult = db.command("serverStatus")
# pprint(serverStatusResult)
#
# app = Flask(__name__)
#
#
# @app.route('/')
# def index_page():
# 	return render_template('index.html')
#
# @app.route("/hello")
# def hello_page():
# 	return "This is the hello world page."
