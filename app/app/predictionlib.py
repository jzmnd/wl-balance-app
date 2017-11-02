# -*- coding: utf-8 -*-
"""
predictionlib.py
Library for W-L balance prediction

Created by Jeremy Smith on 2017-10-04
"""

import sys
import os
from bokeh.plotting import figure
from bokeh.embed import components
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from modellib import compute_mse, BaseResEnsembleEstimator, DataFrameSelector, EstimatorTransformer, ImputeNumber

# Requred to unpickle modellib
sys.path.append('app')


def getData():
    """Import metric data for all ATUS respondents"""
    dfweday = pd.read_csv(os.path.join('app', 'static', 'data', "weday_metrics.csv"),
                          index_col=False)
    dfwehol = pd.read_csv(os.path.join('app', 'static', 'data', "wehol_metrics.csv"),
                          index_col=False)

    return dfweday, dfwehol


def histogramPlot(data, title=None, bins=20, alpha=1.0, prediction=None):
    """Plot a histogram with predicted bar highlighted"""
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

    fig.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
             alpha=alpha, fill_color=colors, line_color=None)

    return fig


def multiPlotOutput(prediction, namedict=None, n=4):
    """Generate Bokeh components for multiple metric plots"""
    plot_weday = []
    plot_wehol = []
    metric_data_weday, metric_data_wehol = getData()

    for i in xrange(n):
        fig_weday = histogramPlot(metric_data_weday['metric{}'.format(i + 1)],
                                  title="Metric {} - {}".format(i + 1, namedict[i + 1]),
                                  bins=50, prediction=prediction[i])

        fig_wehol = histogramPlot(metric_data_wehol['metric{}'.format(i + 1)],
                                  title="Metric {} - {}".format(i + 1, namedict[i + 1]),
                                  bins=50, prediction=prediction[i])

        plot_weday.append(components(fig_weday))
        plot_wehol.append(components(fig_wehol))

    return plot_weday, plot_wehol


def predictScore(demo_input, n=6):
    """Get the predicted scores from the sklearn models"""
    predictions = [0.5, 0.5, 0.5, 0.5, False, False]

    demo_input_u = {key.upper(): float(val) for key, val in demo_input.items()}
    demo_input_df = pd.DataFrame(data=demo_input_u, index=[0], dtype=float)

    model1 = joblib.load(os.path.join('app', 'static', 'models', "pred_model_atus_FULLEST_weday_metric1_2017-11-01.pkl"))
    model2 = joblib.load(os.path.join('app', 'static', 'models', "pred_model_atus_FULLEST_weday_metric2_2017-11-01.pkl"))
    model3 = joblib.load(os.path.join('app', 'static', 'models', "pred_model_atus_FULLEST_weday_metric3_2017-11-02.pkl"))
    model4 = joblib.load(os.path.join('app', 'static', 'models', "pred_model_atus_FULLEST_weday_metric4_2017-11-01.pkl"))

    predictions[0] = model1.predict(demo_input_df)[0]
    predictions[1] = model2.predict(demo_input_df)[0]
    predictions[2] = model3.predict(demo_input_df)[0]
    predictions[3] = model4.predict(demo_input_df)[0]

    return predictions
