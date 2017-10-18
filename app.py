# -*- coding: utf-8 -*-
"""
app.py
Flask app for W-L balance prediction

Created by Jeremy Smith on 2017-10-04
"""

import os
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from flask import Flask, render_template, request
from libs.predictionlib import get_data
from libs.codeslib import *
import pandas as pd


app = Flask(__name__)

PORT = int(os.environ.get('PORT', 33507))

# Create code dictionaries
dfactcodes, dfeducodes, dfinccodes, dfagecodes, dfempcodes, \
    dfindcodes, dfraccodes, dfloccodes, dfwhocodes, dfdemocodes = load_codes()

CODEDICTS = {}
CODEDICTS['ptdtrace'] = [{'name': n, 'value': v} for n, v in zip(dfraccodes.NAME.tolist()[:-5], dfraccodes.CODE.tolist()[:-5])]
CODEDICTS['gestfips'] = [{'name': n, 'value': v} for n, v in zip(dfloccodes.NAME.tolist(), dfloccodes.CODE.tolist())]
CODEDICTS['telfs'] =    [{'name': n, 'value': v} for n, v in zip(dfempcodes.NAME.tolist(), dfempcodes.CODE.tolist())]
CODEDICTS['trdtocc1'] = [{'name': n, 'value': v} for n, v in zip(dfindcodes[dfindcodes.FLAG == 'TRDTOCC1'].NAME.tolist(),
                                                                 dfindcodes[dfindcodes.FLAG == 'TRDTOCC1'].CODE.tolist())]
CODEDICTS['teio1cow'] = [{'name': n, 'value': v} for n, v in zip(dfindcodes[dfindcodes.FLAG == 'TEIO1COW'].NAME.tolist(),
                                                                 dfindcodes[dfindcodes.FLAG == 'TEIO1COW'].CODE.tolist())]
CODEDICTS['peeduca'] = [ {'name': n, 'value': v} for n, v in zip(dfeducodes.NAME.tolist(), dfeducodes.CODE.tolist())]


@app.route('/')
def index():
    html = render_template('index.html')
    return html


# @app.route('/data')
# def data():
#     # returns data here and makes json object
#     return jsonify(get_data())


@app.route('/cluster')
def cluster():
    html = render_template('cluster.html')
    return html


@app.route('/model')
@app.route('/model/<demoinfo>')
def model(demoinfo=None):

    if demoinfo:
        print request.args
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        html = render_template('model-plots.html', codedicts=CODEDICTS,
                               js_resources=js_resources, css_resources=css_resources)

    else:
        html = render_template('model.html', codedicts=CODEDICTS)
    
    return html


@app.route('/about')
def about():
    html = render_template('about.html')
    return html


@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(port=PORT)
