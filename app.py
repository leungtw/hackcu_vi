from flask import Flask, render_template, redirect
from flask import flash, request
from flask import jsonify
import json
app = Flask(__name__)

@app.route('/')
def index_page():
	return render_template('index.html')

@app.route('/home')
def home_page():
	return render_template('index.html')

@app.route('/data')
def data_page():
	return render_template('data.html')

@app.route("/hello")
def hello_page():
	return "This is the hello world page."

@app.route("/submit", methods=['GET', 'POST'])
def submit():
	company = request.form["company"]	
	position = request.form["position"]
	location = request.form["location"]
	link = request.form["link"]
	submitted = request.form["submitted"]
	
	return render_template("data.html")