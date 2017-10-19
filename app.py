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
from libs.predictionlib import getData, histogramPlot
from libs.codeslib import CODEDICTS, FEATURES
import pandas as pd


app = Flask(__name__)

PORT = int(os.environ.get('PORT', 33507))


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

        mm = 'metric2'
        demo_input = request.args

        #prediction = predictScore(mm, demo_input)
        prediction = 0.55

        metric_data_weday, metric_data_wehol = getData(mm)

        fig = histogramPlot(metric_data_weday, title=mm, bins=50, prediction=prediction)

        script, div = components(fig)
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        html = render_template('model-plots.html', codedicts=CODEDICTS,
                               js_resources=js_resources, css_resources=css_resources,
                               plot_script=script, plot_div=div)

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
