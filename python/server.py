import os
import sys

import serial
import pandas as pd


def main(fname):
    if os.path.isfile(fname) and os.path.getsize(fname) > 0:
        df = pd.read_csv(fname, index_col=0)
    else:
        df = pd.DataFrame()

    ser = serial.Serial('/dev/ttyACM0', timeout=1)
    while True:
        raw = ser.readline()
        res = raw.decode('utf-8').rstrip('\n')
        if len(res) == 0: continue
        temp = float(res)
        print('.', end='', flush=True)

        df = df.append({
            'temperature': temp,
            'timestamp': pd.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }, ignore_index=True)
        df.to_csv(fname)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <data file>'.format(sys.argv[0]))
        exit(-1)

    main(sys.argv[1])
