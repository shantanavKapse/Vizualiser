from flask import Flask, render_template, request, redirect
import plotly.express as px
import pandas as pd
from app import app, db
from models import Dashboard
import json


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['data-input']
        d_name = request.form['dashboard-name']
        file.save(f'./files/{d_name}.csv')
        return redirect(f'/preprocess/{d_name}')

    return render_template('index.html')


@app.route('/preprocess/<dboard>', methods=['GET', 'POST'])
def preprocess(dboard):
    df = pd.read_csv(f'./files/{dboard}.csv')
    return render_template('preprocess.html', dashboard_name=dboard, df=df.to_html(justify='center', classes=['table-dark', 'table', 'overflow-auto']))


@app.route('/dashboard/<dboard>', methods=['GET', 'POST'])
def dashboard(dboard):
    df = pd.read_csv(f'./files/{dboard}.csv')
    corr = df.corr()
    heatmap = px.imshow(corr, template='plotly_dark')   # , width=800, height=500
    # json_heatmap = json.dumps(heatmap, cls=plotly.utils.PlotlyJSONEncoder)
    comps = {'dataset': df.to_html(justify='center', classes=['table-dark', 'table', 'overflow-auto']), 'heatmap': heatmap.to_html()}
    return render_template('dashboard.html', comps=comps, dashboard_name=dboard)


@app.route('/dashboards', methods=['GET', 'POST'])
def all_dashboards():
    dsbs = Dashboard.query.all()
    return render_template('dashboards.html', dashboards=dsbs)