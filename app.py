from flask import Flask, render_template, redirect
from flask import flash, request
from flask import jsonify
from pymongo import MongoClient
from pprint import pprint

import json

app = Flask(__name__)
#====== helper methods ======
def setup_mongo_client():
	usr_name = "sale3054"
	pw 	     = "examplepw123"
	client = MongoClient('''mongodb://'''+usr_name+''':'''+ pw +
						 '''@cluster0-shard-00-00-g3da1.mongodb.net:27017,cluster0-shard-00-01-g3da1.mongodb.net:27017,cluster0-shard-00-02-g3da1.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority''')
	return client
#============================

@app.route('/')
def index_page():
	return render_template('index.html')

@app.route('/home')
def home_page():
	return render_template('index.html')

@app.route('/data')
def data_page():
	return render_template('data.html')

@app.route("/submit", methods=['GET', 'POST'])
def submit():

	response = dict(request.form)

	del response["submit"]
	if "submitted" not in response:
		response["submitted"] = "false"
	pprint(response)


	posts = db.posts
	post_id = posts.insert_one(response)
	return redirect("data")

def page_not_found(e):
	return "You suck", e

if __name__ == "__main__":
	app.run(debug=True)

	client = setup_mongo_client()
	db = client.job_db