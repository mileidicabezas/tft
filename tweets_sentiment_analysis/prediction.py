import nltk
import os
import pandas as pd
from scripts.model_evaluation import tokenize
from nltk.corpus import stopwords
from string import punctuation
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer       
from sklearn.svm import LinearSVC
from scripts.sqlite_ops import createConnection, createTable, insertar, contar_regs
import simplejson as json
import datetime

index_table = 2
ubic_json = os.path.join(os.path.abspath("."),'scripts')
ubic_datos = os.path.abspath(".")
table = json.load(open(os.path.join(ubic_json,'tables.json')))[index_table]

campos = [x['name'] for x in table['fields']]
campos.pop(campos.index('id'))
campos = str(tuple(campos)).replace("'","")
ubic_db = os.path.join(ubic_datos, 'tweets.db')

conn = createConnection(ubic_db)
createTable(conn, table)

tweets = pd.read_sql_query('select id, user, lat, long, fec, tweet from raw_tweets where tratado is null',conn)
if(tweets.shape[0] > 0):
    tweets_corpus = pd.read_sql_query("select content, polarity from tweets_corpus where polarity != 'NEU'", conn)
    #tweets_corpus = pd.read_sql_query("select content, polarity from tweets_corpus where polarity", conn)
    nltk.download('stopwords')
    spanish_stopwords = stopwords.words("spanish")
    spanish_stopwords = spanish_stopwords+['algun', 'com', 'contr', 'cuand', 'desd', 'dond', 'durant', 'eram', 'estab', 'estais', 'estam', 'estan', 'estand', 'estaran', 'estaras', 'esteis', 'estem', 'esten', 'estes', 'estuv', 'fuer', 'fues', 'fuim', 'fuist', 'hab', 'habr', 'habran', 'habras', 'hast', 'hem', 'hub', 'mas', 'mia', 'mias', 'mio', 'mios', 'much', 'nad', 'nosotr', 'nuestr', 'par', 'per', 'poc', 'porqu', 'qui', 'seais', 'seam', 'sent', 'ser', 'seran', 'seras', 'si', 'sient', 'sint', 'sobr', 'som', 'suy', 'tambien', 'tant', 'ten', 'tendr', 'tendran', 'tendras', 'teng', 'tien', 'tod', 'tuv', 'tuy', 'vosotr', 'vuestr','tambi']
    #tweets_corpus = tweets_corpus[tweets_corpus.polarity != 'NEU']
    tweets_corpus['polarity_bin'] = 0
    tweets_corpus.polarity_bin[tweets_corpus.polarity.isin(['P', 'P+'])] = 1
    #tweets_corpus.polarity_bin[tweets_corpus.polarity.isin(['NEU'])] = 2
    tweets_corpus.polarity_bin.value_counts(normalize=True)   

    pipeline = Pipeline([
        ('vect', 
        CountVectorizer(
            analyzer='word',
            tokenizer=tokenize,
            lowercase=True,
            stop_words=spanish_stopwords,
            min_df=50,
            max_df=1.9,
            ngram_range=(1,1),
            max_features=1000
        )),
        ('cls', LinearSVC(C=.2, loss='squared_hinge',max_iter=1000,multi_class='ovr',
                random_state=None,
                penalty='l2',
                tol=0.0001
                )),
    ])

    print(datetime.datetime.now())
    pipeline.fit(tweets_corpus.content, tweets_corpus.polarity_bin)
    tweets['polarity'] = pipeline.predict(tweets.tweet)
    print(datetime.datetime.now())
    regs_updatear = []

    #sentiments.to_csv('tweets_sentiments.csv', header=True,index=True)
    regs = []
    for _, row in tweets.iterrows():
        t = (row['user'],row['lat'],row['long'],row['fec'],row['tweet'],row['polarity'])
        regs_updatear.append([row['id']])
        regs.append(t)

    conn.executemany("UPDATE RAW_TWEETS SET TRATADO = 'SI' WHERE ID = ?", regs_updatear)
    insertar(conn, table['name'],campos, regs)    


