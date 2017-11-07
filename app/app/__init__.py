# -*- coding: utf-8 -*-
"""
Flask app for W-L balance prediction

Created by Jeremy Smith on 2017-10-04
"""

from flask import Flask

# Create flask app
app = Flask(__name__)

# Set configurations
app.config.from_object('config')

# Import views
from app import views
