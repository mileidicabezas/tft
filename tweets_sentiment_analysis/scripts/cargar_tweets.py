import os
import simplejson as json
from sqlite_ops import createConnection, createTable, insertar
import csv
import datetime
from pytz import timezone

ubic_datos = os.path.abspath(".")
ubic_json = os.path.join(os.path.abspath("."),'scripts')
ubic_db = os.path.join(ubic_datos, 'tweets.db')
ubic_csv = os.path.join(ubic_datos, 'data.txt')
index_table = 0
table = json.load(open(os.path.join(ubic_json,'/Users/mileidicabezas/Dev/tft_project/final_v_tft/tweets_sentiment_analysis/scripts/tables.json')))[index_table]

conn = createConnection(ubic_db)
createTable(conn, table)

campos = [x['name'] for x in table['fields']]
campos.pop(campos.index('id'))
campos = str(tuple(campos)).replace("'","")

regs = []
with open(ubic_csv) as file:
    rows = csv.reader(file, delimiter='|')
    for row in rows:
        usr = row[0]
        lon = row[1]
        lat = row[2]
        fec = row[3]
        tweet = row[4]
        t = (usr,lon,lat,fec,tweet)
        regs.append(t)

file.close()
insertar(conn, table['name'],campos, regs)