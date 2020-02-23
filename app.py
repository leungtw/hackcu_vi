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

def push_data(data_set, table):
	post_response = table.insert_one(data_set.insert_id)
	return post_response

def select_column_headers(dictionary, approved_columns):
	approved_columns_copy = approved_columns.copy()
	for entry_keys _ in dictionary.values():
		if entry_keys not in approved_columns:
			del approved_columns_copy[entry_key]
	return approved_columns_copy

#============================

@app.route('/')
def index_page():
	return render_template('index.html')

@app.route('/home')
def home_page():
	return render_template('index.html')

@app.route('/dashboard')
def dashboard_page():
	return render_template('dashboard.html')

@app.route('/add')
def add_page():
	return render_template('add.html')

@app.route('/analytics')
def analytics_page():
	return render_template('analytics.html')

@app.route("/submit", methods=['GET', 'POST'])
def submit():
	response = dict(request.form)
	#strip "submit" button data from the request.form
	del response["submit"]
	
	#when the checkbox is unchecked, it will not
	#show the checkbox in the data form, so
	#mark it as false if it was not filled in

	if "submitted" not in response:
		response["submitted"] = "false"

	#send the data to mongoDB
	push_data(response, db.posts)
	#print the form response to the console
	pprint (response)
	posts = db.posts
	post_id = posts.insert_one(response).insert_id
	return redirect("data")


def page_not_found(e):
	return "Something went wrong...", e

if __name__ == "__main__":
	app.run(debug=True)

	client = setup_mongo_client()
	db = client.test_database