import json
import pandas as pd
from flask import Flask, render_template


app = Flask(__name__)

@app.route('/')
def show_entries():
    return render_template('index.html')

@app.route('/data')
def data():
    df = pd.read_csv('../temps.csv', index_col=0)
    return json.dumps(convert(df))

def convert(df):
    res = {'x': [], 'sets': [{'label': 'temperature', 'data': []}]}

    for i, row in df.iterrows():
        res['x'].append(row['timestamp'])
        res['sets'][0]['data'].append(row['temperature'])

    return res


if __name__ == '__main__':
    app.run(host='0.0.0.0')
