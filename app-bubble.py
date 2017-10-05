# -*- coding: utf-8 -*-
"""
app.py
Bubble plot app for W-L balance prediction

Created by Jeremy Smith on 2017-10-05
"""

import os
from flask import Flask, render_template, request


app = Flask(__name__)

PORT = int(os.environ.get('PORT', 8000))


@app.route('/')
def index():

    # Render html template
    html = render_template('bubble.html')

    return html


if __name__ == '__main__':
    app.run(port=PORT)
