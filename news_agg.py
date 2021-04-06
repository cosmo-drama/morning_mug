#! /home/sphinx/projects/morning_mug/venv/venv/bin/python3
from flask import Flask, render_template
import time
import os
from datetime import datetime
from os import listdir
import json

data_path = '/home/athena/projects/morning_mug/data'

app = Flask(__name__)
@app.route('/', methods=["GET"])
def index():
    data_dict = {}
    for i in listdir(data_path):
        with open(data_path + "/" + i) as f:
            data_files = json.load(f)
            data_dict[str(i)] = data_files


    return render_template('index.html', data=data_dict)

@app.after_request
def add_header(response):

    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'

    return response

@app.cli.command()
def scheduled():
    """Run scheduled tasks."""
    now = datetime.utcnow()
    print(now)
    print('Updating Database(.json files)...')
    from updated_scraper import fetch_data, save_data
    time.sleep(5)
    print('Done!')