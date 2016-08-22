import os

import serial
import pandas as pd


DATA_FILE = '../temps.csv'

def main():
    if os.path.isfile(DATA_FILE):
        df = pd.read_csv(DATA_FILE, index_col=0)
    else:
        df = pd.DataFrame()

    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    while True:
        raw = ser.readline()
        res = raw.decode('utf-8').rstrip('\n')
        if len(res) == 0: continue
        temp = float(res)

        df = df.append({
            'temperature': temp,
            'timestamp': pd.datetime.now()
        }, ignore_index=True)
        df.to_csv(DATA_FILE)

if __name__ == '__main__':
    main()
