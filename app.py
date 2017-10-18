# -*- coding: utf-8 -*-
"""
app.py
Flask app for W-L balance prediction

Created by Jeremy Smith on 2017-10-04
"""

import os
#from bokeh.plotting import figure
#from bokeh.embed import components
#from bokeh.resources import INLINE
#from bokeh.util.string import encode_utf8
from flask import Flask, render_template, request
from predictionlib import get_data


app = Flask(__name__)

PORT = int(os.environ.get('PORT', 33507))


@app.route('/')
def index():
    # Render html template
    html = render_template('index.html')
    return html


# @app.route('/data')
# def data():
#     # returns data here and makes json object
#     return jsonify(get_data())


@app.route('/cluster')
def cluster():
    # Render html template
    html = render_template('cluster.html')
    return html


@app.route('/model')
def model():
    # Render html template
    html = render_template('model.html')
    return html


@app.route('/about')
def about():
    # Render html template
    html = render_template('about.html')
    return html


@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(port=PORT)
