# -*- coding: utf-8 -*-
"""
Flask app for W-L balance prediction

Created by Jeremy Smith on 2017-10-04
"""

from flask import Flask

app = Flask(__name__)

# Configurations
app.config.from_object('config')

from app import views
