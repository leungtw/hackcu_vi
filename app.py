from flask import Flask, render_template, redirect
from flask import flash, request
from flask import jsonify
from pymongo import MongoClient
from pprint import pprint
from bs4 import BeautifulSoup

import json
import requests
import re
	
app = Flask(__name__)
#====== helper methods ======
def setup_mongo_client():
	usr_name = "sale3054"
	pw 	     = "examplepw123"
	client = MongoClient('''mongodb://'''+usr_name+''':'''+ pw +
						 '''@cluster0-shard-00-00-g3da1.mongodb.net:27017,cluster0-shard-00-01-g3da1.mongodb.net:27017,cluster0-shard-00-02-g3da1.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority''')
	return client

def push_data(data_set, table):
	post_response = table.insert_one(data_set)
	return post_response

def select_column_headers(dictionary, approved_columns):
	dict_copy = dictionary.copy()
	for entry_key in dictionary.keys():
		if entry_key not in approved_columns:
			del dict_copy[entry_key]
	return dict_copy

def get(collection):
    documents = collection.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return json.loads(json.dumps(response))

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
	information = { "company": "", "position": "", "location": ""}
	return render_template('add.html', information=information)

@app.route('/analytics')
def analytics_page():
	return render_template('analytics.html')

@app.route("/submit", methods=['GET', 'POST'])
def submit():

	table_contents = get(db.posts)
	print(type(table_contents))
	
	response = dict(request.form)
	approved_column_headers = ["company", 
	                           "position", 
	                           "location", 
							   "link", 
						       "submitted"]
	
	response = select_column_headers(response, 
								     approved_column_headers)
	
	# when the checkbox is unchecked, it will not
	# show the checkbox in the data form, so
	# mark it as false if it was not filled in
	approved_column_headers.insert(0, "_id")

	if "submitted" not in response:
		response["submitted"] = "false"
	print("response: ", response)
	print("table_contents: ", table_contents)
	#send the data to mongoDB
	push_data(response, db.posts)
	#print the form response to the console
	print(list(table_contents))
	return render_template("dashboard.html", table_contents=table_contents, approved_column_headers=approved_column_headers)


@app.route('/scrape_linkedin', methods=['GET', 'POST'])
def scrape():
	url = request.form["link"]
	page = requests.get(url).text
	soup = BeautifulSoup(page, "html.parser")

	title = soup.find('title')
	title_str = str(title)

	if title_str is None:
		return render_template('add.html')

	# <title>Brooksource hiring Data Analyst in Stamford, Connecticut, United States | LinkedIn</title>
	print(title_str)

	company = title_str[title_str.find('<title>')+7 : title_str.find(' ')]
	position = title_str[title_str.find('hiring ')+7 : title_str.find(' in')]
	location = title_str[title_str.find(', ')+2 : title_str.find(', United States')]

	print(company + position + location)

	information = { "company": company, "position": position, "location": location, "link":str(url)}

	return render_template('add.html', information=information)

def page_not_found(e):
	return "Something went wrong...", e

if __name__ == "__main__":
	client = setup_mongo_client()
	db = client.job_db
	app.run(debug=False)

