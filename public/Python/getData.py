#!flask/bin/python
from flask import Flask, session
from flask import request
from flask import abort
from flask_cors import CORS
from math import sqrt
app = Flask(__name__)
cors = CORS(app, resources={r"/getData.py": {"origins": "http://localhost:3000"}})

@app.route('/getData.py', methods=['POST'])

def getData():
    
    import psycopg2
    import os
    import json

    print request.data
    if not request.data or request.data not in set(['ITR', 'ROL', 'PAN', 'AMD']):
       abort(400)
    
    HOST = 'hindsight-test-pan-3.cun2acaa3ktx.us-east-1.redshift.amazonaws.com'
    PORT = 5439 # redshift default
    USER = 'juno'
    PASSWORD = '@Jun0p@ass!'
    DATABASE = 'cdtos'

    def db_connection():
        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
        )
        return conn

    def json_load_byteified(file_handle):
        return _byteify(
            json.load(file_handle, object_hook=_byteify),
            ignore_dicts=True
        )

    def json_loads_byteified(json_text):
        return _byteify(
            json.loads(json_text, object_hook=_byteify),
            ignore_dicts=True
        )

    def _byteify(data, ignore_dicts = False):
        # if this is a unicode string, return its string representation
        if isinstance(data, unicode):
            return data.encode('utf-8')
        # if this is a list of values, return list of byteified values
        if isinstance(data, list):
            return [ _byteify(item, ignore_dicts=True) for item in data ]
        # if this is a dictionary, return dictionary of byteified keys and values
        # but only if we haven't already byteified it
        if isinstance(data, dict) and not ignore_dicts:
            return {
                _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
                for key, value in data.iteritems()
            }
        # if it's anything else, return it in its original form
        return data
    
    def getTrendData(fileName):
        fileName = "../json/" + fileName
        g = open(fileName, mode='rt')
        h = g.read()
        k = json_loads_byteified(h)
        l = len(k["region_cd"])
        w, h = 2, l
        Matrix = [[0 for x in range(w)] for y in range(h)]
        for i in range(0,l):
            try:
                s = str(i)
                if k["region_cd"][s] is not '':
                    Matrix[i][0] = int(k["region_cd"][s])
                    Matrix[i][1] = k["sum"][s]/1000000000
                    
            except KeyError, e:
                pass
        g.close()
        if request.data == 'PAN':
            f = open('../json/trends.json',mode='wt')
        elif request.data == 'ITR':
            f = open('../json/trends2.json',mode='wt')
        elif request.data == 'AMD':
            f = open('../json/trends3.json',mode='wt')
        elif request.data == 'ROL':
            f = open('../json/trends4.json',mode='wt')
                    
        f.seek(0)
        f.truncate()
        Matrix.sort()
        f.write("[\n")
        i = 0
        z = 0
        a = 0
        for item in Matrix:
            z = a+1
            for u in range(a+1,(Matrix[i][0])):
                f.write("[%s, 0]" %z)
                f.write(",\n")
                z = z + 1
            f.write("%s" % item)
            a = Matrix[i][0]
            i = i + 1
            if i != l:
                f.write(",\n")

        f.write("]")
        f.close()
        
    # using pandas
    import pandas as pd
    conn = db_connection()
    try:
        if request.data == 'PAN':
            example_query = "select f.region_cd, sum(total_value_rounded) from hindsight_3.value_dim v, hindsight_3.fact_event f where f.event_type='PAN' and f.effective_dte='2017-01-01' and f.fact_id = v.fact_id group by f.region_cd;"
            df = pd.read_sql(example_query, conn)
            df.to_json(path_or_buf='../json/PAN.json')
            getTrendData('PAN.json')
        elif request.data == 'ITR':
            example_query = "select f.region_cd, sum(total_value_rounded) from hindsight_3.value_dim v, hindsight_3.fact_event f where f.event_type='ITR' and f.effective_dte='2017-01-01' and f.fact_id = v.fact_id group by f.region_cd;"
            df = pd.read_sql(example_query, conn)
            df.to_json(path_or_buf='../json/ITR.json')
            getTrendData('ITR.json')
        elif request.data == 'AMD':
            example_query = "select f.region_cd, sum(total_value_rounded) from hindsight_3.value_dim v, hindsight_3.fact_event f where f.event_type='AMD' and f.effective_dte='2017-01-01' and f.fact_id = v.fact_id group by f.region_cd;"
            df = pd.read_sql(example_query, conn)
            df.to_json(path_or_buf='../json/AMD.json')
            getTrendData('AMD.json')
        elif request.data == 'ROL':
            example_query = "select f.region_cd, sum(total_value_rounded) from hindsight_3.value_dim v, hindsight_3.fact_event f where f.event_type='ROL' and f.effective_dte='2017-01-01' and f.fact_id = v.fact_id group by f.region_cd;"
            df = pd.read_sql(example_query, conn)
            df.to_json(path_or_buf='../json/ROL.json')
            getTrendData('ROL.json')
    finally:
        conn.close()

    return 'success'
    
if __name__ == '__main__':
    app.run(debug=True)