from flask import Flask, render_template, redirect, flash, request
import requests
import json
app = Flask(__name__)

@app.route('/')
def index_page():
	return render_template('index.html')