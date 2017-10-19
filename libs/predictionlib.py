# -*- coding: utf-8 -*-
"""
predictionlib.py
Library for W-L balance prediction

Created by Jeremy Smith on 2017-10-04
"""

import os
from bokeh.plotting import figure
import numpy as np
import pandas as pd


def getData(m):
    # Import metric data
    dfweday = pd.read_csv(os.path.join('static', 'data', "weday_metrics.csv"),
                             index_col=False)
    dfwehol = pd.read_csv(os.path.join('static', 'data', "wehol_metrics.csv"),
                             index_col=False)

    return dfweday[m], dfwehol[m]


def histogramPlot(data, title=None, bins=20, alpha=1.0, prediction=None):
    fig = figure(title=title,
             x_axis_label='Score', y_axis_label='Frequency',
             plot_height=100, plot_width=400,
             sizing_mode='scale_width')

    hist, edges = np.histogram(data, density=True, bins=bins)
    colors = ['#aaaaaa'] * bins

    if prediction:
        if prediction <= 0:
            i = 0
        elif prediction >= 1:
            i = bins - 1
        else:
            i = np.digitize(prediction, edges) - 1
        colors[i] = '#337ab7'

    fig.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], alpha=alpha, fill_color=colors, line_color=None)

    return fig
