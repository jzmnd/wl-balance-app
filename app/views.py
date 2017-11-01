# -*- coding: utf-8 -*-
"""
views.py for W-L balance prediction app

Created by Jeremy Smith on 2017-10-30
"""

from app import app
from bokeh.resources import INLINE
from flask import render_template, request
from predictionlib import multiPlotOutput, predictScore
from codeslib import CODEDICTS, METRICNAMES


@app.route('/')
def index():
    html = render_template('index.html')
    return html


@app.route('/cluster')
def cluster():
    html = render_template('cluster.html')
    return html


@app.route('/model')
@app.route('/model/<demoinfo>')
def model(demoinfo=None):

    if demoinfo:
        demo_input = request.args
        prediction = predictScore(demo_input)
        plot_weday, plot_wehol = multiPlotOutput(prediction, namedict=METRICNAMES)

        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        html = render_template('model-plots.html', codedicts=CODEDICTS,
                               js_resources=js_resources, css_resources=css_resources,
                               plot_script1=plot_weday[0][0], plot_div1=plot_weday[0][1],
                               plot_script2=plot_weday[1][0], plot_div2=plot_weday[1][1],
                               plot_script3=plot_weday[2][0], plot_div3=plot_weday[2][1],
                               plot_script4=plot_weday[3][0], plot_div4=plot_weday[3][1])

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
