import os
import sys
import json

import pandas as pd

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app, async_mode='threading')

@app.route('/')
def show_entries():
    return render_template('index.html')

@app.route('/data')
def data():
    return get_data()

def get_data():
    df = pd.read_csv(DATA_FILE, index_col=0)
    return json.dumps(convert(df))

def convert(df):
    res = {'x': [], 'sets': [{'label': 'temperature', 'data': []}]}

    for i, row in df.iterrows():
        res['x'].append(row['timestamp'])
        res['sets'][0]['data'].append(row['temperature'])

    return res

class FileObserver(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == DATA_FILE:
            socketio.emit('update', get_data())

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <data file>'.format(sys.argv[0]))
        exit(-1)
    DATA_FILE = sys.argv[1]

    observer = Observer()
    observer.schedule(
        FileObserver(),
        path=os.path.dirname(DATA_FILE), recursive=False)
    observer.start()

    socketio.run(app)
