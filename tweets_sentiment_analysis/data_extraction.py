import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import datetime
from pytz import timezone
from scripts.sqlite_ops import createConnection, createTable, insertar
import os
import pandas as pd

consumer_key = 'consumer_key'
consumer_secret = 'consumer_secret'
acces_token = 'acces_token'
acces_secret = 'acces_secret'
ubication = [-78.645630,-0.296630,-78.370972,-0.104370]
quito_by_default = [-0.229498, -78.524300]


index_table = 0
ubic_json = os.path.join(os.path.abspath("."),'scripts')
ubic_datos = os.path.abspath(".")
table = json.load(open(os.path.join(ubic_json,'tables.json')))[index_table]

campos = [x['name'] for x in table['fields']]
campos.pop(campos.index('id'))
campos.pop(campos.index('tratado'))
campos = str(tuple(campos)).replace("'","")
ubic_db = os.path.join(ubic_datos, 'tweets.db')

conn = createConnection(ubic_db)
createTable(conn, table)

def generar_tweets_heatmap():
    min_lat = -0.296630
    max_lat = -0.104370
    min_lon = -78.645630
    max_lon = -78.370972
    loc = pd.read_sql_query("select lat, long from raw_tweets", createConnection(ubic_db))
    tweets = loc[(loc['long'] > min_lon) & (loc['long'] < max_lon) & (loc['lat'] > min_lat) & (loc['lat'] < max_lat)]

    with open('tweets_heatmap','w') as file:
        file.write(tweets.to_string(header=False, index=False))
    file.close()    

class listener(StreamListener):

    def on_data(self, data):
    
        try:
            decoded = json.loads(data)
        except Exception as e:
            print (e) 
            return True
   
        if decoded.get('geo') is not None:
            location = decoded.get('geo').get('coordinates')
        else:
            location = str(quito_by_default)
        text = decoded['text'].replace('\n',' ')
        
        user = '@' + decoded.get('user').get('screen_name')
        
        lon, lat = ('','')
        
        if isinstance(location, list):
            lon = location[0]
            lat = location[1]
        else:
            loc = location.replace('[','').replace(']','').split(',')
            lon = loc[0]
            lat = loc[1]

        created = decoded.get('created_at')
        fec = datetime.datetime.strptime(created, '%a %b %d %H:%M:%S %z %Y')
        fec = fec.astimezone(timezone('America/Guayaquil'))
        regs = []
        t = (user, lon, lat, fec, text)
        print('%s|%s|%s|%s|%s' %(user, lon, lat, fec.strftime('%a %b %d %H:%M:%S %z %Y'),text))
        regs.append(t)
        insertar(conn, table['name'],campos, regs)
        generar_tweets_heatmap()

        return True

    def on_error(self, status):
        print (status)
 
if __name__ == '__main__':
    print('Empezando...')
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(acces_token, acces_secret)
    twitterStream = Stream(auth, listener())
    twitterStream.filter(locations=ubication, languages=["es"])
