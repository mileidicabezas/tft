import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
from scripts.sqlite_ops import createConnection, createTable, insertar, truncar, cerrar
import matplotlib.pyplot as plt

import os
import simplejson as json

ubic_datos = path.abspath(".")
ubic_db = path.join(ubic_datos, 'tweets.db')
conn = createConnection(ubic_db)
l_hashtags = []
dict_htg = {}

tweets = pd.read_sql_query('select id, tweet from raw_tweets', conn)
for _, row in tweets.iterrows():
    tweet = row['tweet']
    tweet_id = row['id']
    tweet = tweet.strip()
    tiene_hashtag = False

    seguir = True    
    while (seguir):
        tiene_hashtag = False
        pos_hastag = tweet.find('#')
        if pos_hastag < 0 and not tiene_hashtag:
            seguir = False
            if 'Ninguno' not in dict_htg.keys():
                dict_htg = {'Ninguno':{'num_repeticiones':1, 'tweets':[tweet_id]}}
            else:
                dict_htg['Ninguno']['num_repeticiones'] += 1
                dict_htg['Ninguno']['tweets'].append(tweet_id)
        else:
            if pos_hastag >= 0:
                tiene_hashtag = True
                aux_tweet = tweet[pos_hastag+1:]
                pos_fin = aux_tweet.find(' ')
                if pos_fin < 0: pos_fin = len(aux_tweet)
                hash_tag = aux_tweet[:pos_fin].replace(".","").replace(",","")
                #if hash_tag == 'QuitoPatrimonioMío':
                #    print("aqui nos paramos")
                l_hashtags.append(hash_tag)
                if hash_tag not in dict_htg.keys() and len(dict_htg.keys()) == 0:
                    if(hash_tag == ' '): hash_tag='#'
                    dict_htg = {hash_tag:{'num_repeticiones':1, 'tweets':[tweet_id]}}                
                else:
                    if hash_tag not in dict_htg.keys():
                        if(hash_tag == ' '): hash_tag='#'
                        dict_htg[hash_tag] = {}
                        dict_htg[hash_tag]['num_repeticiones'] = 1
                        dict_htg[hash_tag]['tweets'] = [tweet_id]
                    else:
                        if tweet_id not in dict_htg[hash_tag]['tweets']:
                            if(hash_tag == ' '): hash_tag='#'
                            dict_htg[hash_tag]['num_repeticiones'] += 1
                            dict_htg[hash_tag]['tweets'].append(tweet_id)
            

            

            tweet = aux_tweet
            if len(tweet) == 0 or tweet.find('#') < 0:
                seguir = False



dict_hashtags = {'hashtags':l_hashtags}
df_hashtags = pd.DataFrame(data=dict_hashtags)
text = ' '.join(h for h in df_hashtags.hashtags)
wordcloud = WordCloud(max_font_size=150, height=640, width=1024, max_words=999, collocations=False).generate(text)
wordcloud.to_file('hashtags.png')
l_records = [((x, dict_htg[x]['num_repeticiones'])) for x in dict_htg.keys() if dict_htg[x]['num_repeticiones']]
l_records2 = []

for k in dict_htg.keys():
    for t in dict_htg[k]['tweets']:
        l_records2.append((k,t))
    

index_table = 3
ubic_json = os.path.join(os.path.abspath("."),'scripts')
ubic_datos = os.path.abspath(".")
table = json.load(open(os.path.join(ubic_json,'tables.json')))[index_table]

campos = [x['name'] for x in table['fields']]
campos = str(tuple(campos)).replace("'","")

createTable(conn, table)
truncar(conn, table['name'])

campos = [x['name'] for x in table['fields'] if x['name'] != 'id']
campos = str(tuple(campos)).replace("'","")

insertar(conn, table['name'],campos, l_records)

index_table = 4
ubic_json = os.path.join(os.path.abspath("."),'scripts')
ubic_datos = os.path.abspath(".")
table = json.load(open(os.path.join(ubic_json,'tables.json')))[index_table]

campos = [x['name'] for x in table['fields']]
campos = str(tuple(campos)).replace("'","")

createTable(conn, table)
truncar(conn, table['name'])

campos = [x['name'] for x in table['fields'] if x['name'] != 'id']
campos = str(tuple(campos)).replace("'","")
insertar(conn, table['name'],campos, l_records2)
