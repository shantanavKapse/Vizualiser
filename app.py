from flask import Flask, render_template, request, redirect, flash
import plotly.express as px
import pandas as pd
import numpy as np
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import plotly
import json
from sklearn.preprocessing import MinMaxScaler , StandardScaler

app = Flask(__name__)

app.secret_key = b'hackenthonkriyeta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)


from models import Dashboard, Component


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['data-input']
        d_name = request.form['dashboard-name']
        file.save(f'./files/{d_name}.csv')
        df = pd.read_csv(f'./files/{d_name}.csv', encoding='latin')
        corr = df.select_dtypes(exclude='object').corr()
        heatmap = px.imshow(corr, template='plotly_dark')
        json_heatmap = json.dumps(heatmap, cls=plotly.utils.PlotlyJSONEncoder)
        dsb = Dashboard(name=d_name, file_name=f'{d_name}.csv')
        db.session.add(dsb)
        db.session.commit()
        curr_dsb = Dashboard.query.filter_by(name=d_name).first()
        com = Component(name="heatmap", dashboard_id=curr_dsb.id, data=json_heatmap)
        db.session.add(com)
        db.session.commit()
        return redirect(f'/preprocess/{d_name}')

    return render_template('index.html')


@app.route('/preprocess/<dboard>', methods=['GET', 'POST'])
def preprocess(dboard):
    if request.method == 'POST':
        print(request.form)
    df = pd.read_csv(f'./files/{dboard}.csv')
    col = df.columns[df.isnull().any()]
    null_col = []
    for column in col:
        temp_dct = {
            'column': column,
            'number_null': df[column].isnull().sum(),
            'mean_fill': False
        }
        dtn = df[column].dtype.name
        if ('int' in dtn) or 'float' in dtn:
            temp_dct['mean_fill'] = True
        null_col.append(temp_dct)

    # print(df.describe().)

    return render_template('preprocess.html', dashboard_name=dboard, null_col=null_col, df_info=df.describe().to_html(justify='center', classes=['table-dark', 'table', 'overflow-auto', 'mb-0']))


@app.route('/dashboard/<dboard>', methods=['GET', 'POST'])
def dashboard(dboard):
    df = pd.read_csv(f'./files/{dboard}.csv')
    curr_dsb = Dashboard.query.filter_by(name=dboard).first()
    if request.method == 'POST':
        data = request.form
        ct = data['chart-type']
        x = data['x-col']
        y = data['y-col']
        clr = data['color']
        if clr == '0':
            clr = None
        # x_label = data['x-label']
        # y_label = data['y-label']
        ttl = data['title']
        if ct == '1':
            fig = px.histogram(df, x=x, y=y, title=ttl, labels={x: x, y: y}, color=clr, barmode='group', template='plotly_dark', histfunc='avg')
        elif ct == '2':
            if data['add_regression']:
                fig = px.scatter(df, x=x, y=y, title=ttl, labels={x: x, y: y}, color=clr, template='plotly_dark', trendline='ols', trendline_color_override='red')
            else:
                fig = px.scatter(df, x=x, y=y, title=ttl, labels={x: x, y: y}, color=clr, template='plotly_dark')
        elif ct == '3':
            print(y)
            if y != 'Select column for y-axis':
                fig = px.pie(df, values=y, names=x, title=ttl, labels={x: x, y: y}, color=clr, template='plotly_dark')
            else:
                fig = px.pie(df, names=x, title=ttl, labels={x: x}, color=clr, template='plotly_dark')
        elif ct == '4':
            fig = px.histogram(df, x=x, title=ttl, labels={x: x}, color=clr, template='plotly_dark')
        elif ct == '5':
            fig = px.violin(df, x=x, y=y, title=ttl, labels={x: x, y: y}, color=clr, template='plotly_dark')
        elif ct == '6':
            fig = px.box(df, x=x, y=y, title=ttl, labels={x: x, y: y}, color=clr, template='plotly_dark')
        else:
            fig = px.line(df, x=x, y=y, title=ttl, labels={x: x, y: y}, color=clr, template='plotly_dark')
        json_fig = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        com = Component(name=ttl, dashboard_id=curr_dsb.id, data=json_fig)
        db.session.add(com)
        db.session.commit()
        flash(message='Successfully added the chart to dashboard!', category='success')
        return redirect(f'/dashboard/{dboard}')

    num_cols = [col for col in df.columns if 'int' in df[col].dtype.name or 'float' in df[col].dtype.name]
    cat_cols = [col for col in df.columns if 'int' not in df[col].dtype.name and 'float' not in df[col].dtype.name]
    cols = list(df.columns)
    components = Component.query.filter_by(dashboard_id=curr_dsb.id).all()
    # comps = {'dataset': df.to_html(justify='center', classes=['table-dark', 'table', 'overflow-auto'])}
    comps = [{'name': 'dataset', 'data': df.to_html(justify='center', classes=['table-dark', 'table', 'overflow-auto']), 'id': "dataset"}]
    for c in components:
        cd = {'name': c.name, 'data': plotly.io.from_json(c.data).to_html(), 'id': c.id}
        comps.append(cd)
    return render_template('dashboard2.html', comps=comps, dashboard_name=dboard, cat_cols=cat_cols, num_cols=num_cols, cols=cols)


@app.route('/dashboards', methods=['GET', 'POST'])
def all_dashboards():
    dsbs = Dashboard.query.all()
    return render_template('dashboards.html', dashboards=dsbs)


@app.route('/process-value', methods=['POST'])
def process():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)
            df = pd.read_csv(f'./files/{data["dashboard_name"]}.csv')
            for o in data['data']:
                print(o['selection'])
                if o['selection'] == 'back-fill':
                    df[o['column_name']].fillna(method='backfill', inplace=True)
                elif o['selection'] == 'front-fill':
                    df[o['column_name']].fillna(method='ffill', inplace=True)
                elif o['selection'] == 'remove-row':
                    print(o['column_name'])
                    df.dropna(subset=[o['column_name']], inplace=True)
                elif o['selection'] == 'user-entry':
                    dname = df[o['column_name']].dtype.name
                    fillvalue = o['manual_input']
                    # if 'int' in dname:
                    #     if o['manual_input'] == '':
                    #         fillvalue = 0
                    #     else:
                    #         fillvalue = int(fillvalue)
                    # elif 'float' in dname:
                    #     if o['manual_input'] == '':
                    #         fillvalue = 0.0
                    #     else:
                    #         fillvalue = float(fillvalue)
                    df[o['column_name']].fillna(value=fillvalue, inplace=True)
                elif o['selection'] == 'mean-fill':
                    dname = df[o['selection']].dtype.name
                    if 'int' in dname or 'float' in dname:
                        df[o['selection']].fillna(value=df[o['selection']].mean(), inplace=True)

            int_col = df.select_dtypes(include=['int', 'float']).columns.tolist()
            scale = data['scale']
            scale_type = data['scale-type']
            if scale is True and scale_type == 'min-max':
                df[int_col] = MinMaxScaler().fit_transform(df[int_col])
            if scale is True and scale_type == 'standard':
                df[int_col] = StandardScaler().fit_transform(df[int_col])
            print(data['scale'], data['scale-type'])
            df.to_csv(f'./files/{data["dashboard_name"]}.csv', index=False)
            return json.dumps({'status': 200, 'message': "Success"})
        except Exception as e:
            return json.dumps({'status': 500, 'message': str(e)})


@app.route('/delete-comp/<dashname>/<int:id>', methods=['GET'])
def delete_component(dashname, id):
    c = Component.query.filter_by(id=id).first()
    db.session.delete(c)
    db.session.commit()
    flash('Component deleted successfully!', 'success')
    return redirect(f"/dashboard/{dashname}")


if __name__ == '__main__':
    app.run(debug=True)
