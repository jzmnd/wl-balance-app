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


app = Flask(__name__)


PORT = int(os.environ.get('PORT', 33507))


@app.route('/')
def index():

    # Bokeh script, div, js and css components to send to html template
    script, div = components(fig)
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # Render html template
    html = render_template('index.html', plot_script=script, plot_div=div,
                           js_resources=js_resources, css_resources=css_resources,
                           ticker=ticker, graphtyp=graphtyp, graphtyps=GRAPHTYPLIST)

    return encode_utf8(html)


@app.route('/data')
def data():
    return jsonify(get_data())


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(port=PORT)
