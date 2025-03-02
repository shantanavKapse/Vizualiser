import json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask import Flask, render_template, request
import plotly.express as px
import plotly
import pandas as pd

app = Flask(__name__)

df = None


app.secret_key = b'hackenthonkriyeta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['data-inp']
        global df
        df = pd.read_csv(file.stream)
        corr = df.corr()
        heatmap = px.imshow(corr, template='plotly_dark', width=800, height=400)
        json_heatmap = json.dumps(heatmap, cls=plotly.utils.PlotlyJSONEncoder)
        return {'df': df.to_json(), 'heatmap': json_heatmap}

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
