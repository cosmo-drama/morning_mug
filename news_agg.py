
from flask import Flask, render_template
from init_db import vice, itsnicethat, pitchfork, the_verge, wired, ars_technica


app = Flask(__name__)
@app.route('/', methods=["GET"])
def index():
    data_dict = {}
    data_dict['the-verge'] = the_verge
    data_dict['vicenews'] = vice
    data_dict['wired'] = wired
    data_dict['itsnicethat'] = itsnicethat
    data_dict['arstechnica'] = ars_technica
    data_dict['pitchfork'] = pitchfork


    return render_template('index.html', data=data_dict)

@app.after_request
def add_header(response):

    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'

    return response