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
	
	response = dict(request.form)
	approved_column_headers = ["company", 
	                           "position", 
	                           "location", 
							   "link", 
						       "submitted"]
	
	response = select_column_headers(response, 
								     approved_column_headers)
	state_list = ['Alabama',
					'Alaska', 
					'Arizona', 
					'Arkansas', 
					'California',
					'Colorado', 
					'Connecticut',
					'Delaware', 
					'Florida', 
					'Georgia',
					'Hawaii', 
					'Idaho', 
					'Illinois', 
					'Indiana', 
					'Iowa', 
					'Kansas', 
					'Kentucky',
					'Louisiana', 
					'Maine', 
					'Maryland',
					'Massachusetts', 
					'Michigan', 
					'Mississippi', 
					'Missouri', 
					'Minnesota', 
					'Montana',
					'Nebraska', 
					'Nevada', 
					'New Hampshire', 
					'New Jersey', 
					'New Mexico', 
					'New York', 
					'North Carolina',
					'North Dakota', 
					'Ohio', 
					'Oklahoma', 
					'Oregon', 
					'Pennsylvania', 
					'Rhode Island', 
					'South Carolina', 
					'South Dakota', 
					'Tennessee', 
					'Texas',
					'Utah', 
					'Vermont', 
					'Virginia', 
					'Wyoming',
					'Washington',
					'Wisconsin',
					'West Virginia']

	state_dict = {}
	for state in state_list:
		tmp_dct = {"location" : state }
		dict_count = db.posts.find(tmp_dct).count()
		state_dict[state] = dict_count
	state_dict_vals = []
	for state in state_list:
		state_dict_vals.append(state_dict[state])

	in_progress = db.posts.find({"submitted": "In Progress"}).count()
	subbed = db.posts.find({"submitted" : "Submitted"}).count()
	respnd = db.posts.find({"submitted" : "Responded"}).count()
	_offer = db.posts.find({"submitted" : "Offer"}).count()
	_reject = db.posts.find({"submitted" : "Rejected"}).count()
	_interview = db.posts.find({"submitted" : "Interview Ongoing"}).count()

	print(in_progress, subbed, respnd)
	
	# when the checkbox is unchecked, it will not
	# show the checkbox in the data form, so
	# mark it as false if it was not filled in
	approved_column_headers.insert(0, "_id")

	if "submitted" not in response:
		response["submitted"] = "None Selected"
	#send the data to mongoDB
	push_data(response, db.posts)
	return render_template("dashboard.html", 
							table_contents=table_contents, 
						 	approved_column_headers=approved_column_headers,
							state_dict=state_dict,
							state_dict_vals=state_dict_vals,
							in_progress=in_progress, subbed=subbed, respnd=respnd,
							_offer = _offer, _reject=_reject, _interview=_interview)


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

