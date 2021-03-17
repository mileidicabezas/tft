
import datetime

import pandas as pd
import sys
import os
from lxml import objectify
import simplejson as json

import nltk
from nltk.corpus import stopwords
from string import punctuation
from sklearn.feature_extraction.text import CountVectorizer       
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

from sklearn.model_selection import cross_val_score, GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

pd.set_option('max_colwidth',1000)
mypath = os.path.join(os.getcwd(),'TSS')
here = os.path.join(os.getcwd(),'scripts/CSVS/')

def obtencionDatos():
    try:
        general_tweets_corpus_train = pd.read_csv(os.path.join(here,'general-tweets-train-tagged.csv'), encoding="UTF-8")
    except:
        xml = objectify.parse(open(os.path.join(mypath,'general-train-tagged.xml')))
        root = xml.getroot()
        general_tweets_corpus_train = pd.DataFrame(columns=('content', 'polarity', 'agreement'))
        tweets = root.getchildren()
        for i in range(0,len(tweets)):
            tweet = tweets[i]
            row = dict(zip(['content', 'polarity', 'agreement'], [tweet.content.text, tweet.sentiments.polarity.value.text, tweet.sentiments.polarity.type.text]))
            row_s = pd.Series(row)
            row_s.name = i
            general_tweets_corpus_train = general_tweets_corpus_train.append(row_s)
        general_tweets_corpus_train.to_csv('general-tweets-train-tagged.csv', index=False, encoding='utf-8')

    try:
        general_tweets_corpus_test = pd.read_csv(os.path.join(here,'general-tweets-test-tagged.csv'), encoding='utf-8')
    except:    
        xml = objectify.parse(open(os.path.join(mypath,'general-test-tagged.xml')))
        root = xml.getroot()
        general_tweets_corpus_test = pd.DataFrame(columns=('content', 'polarity'))
        tweets = root.getchildren()
        print("Total de Registros: "+str(len(tweets)))
        x = 1
        for i in range(0,len(tweets)):
            if(x%5000 == 0): print("Registros tratados: "+str(x))
            tweet = tweets[i]
            row = dict(zip(['content', 'polarity', 'agreement'], [tweet.content.text, tweet.sentiments.polarity.value.text]))
            row_s = pd.Series(row)
            row_s.name = i
            x+=1
            general_tweets_corpus_test = general_tweets_corpus_test.append(row_s)
        print("Registros tratados: "+str(x-1))
        general_tweets_corpus_test.to_csv(os.path.join(here,'general-tweets-test-tagged.csv'), index=False, encoding='utf-8')  

    try:
        stompol_tweets_corpus_train = pd.read_csv(os.path.join(here,'stompol-tweets-train-tagged.csv'), encoding='utf-8')  
    except:    
        xml = objectify.parse(open(os.path.join(mypath,'stompol-test-tagged.xml')))
        root = xml.getroot()
        stompol_tweets_corpus_train = pd.DataFrame(columns=('content', 'polarity'))
        tweets = root.getchildren()
        print("Total de Registros: "+str(len(tweets)))
        x = 1
        for i in range(0,len(tweets)):
            if(x%5000 == 0): print("Registros tratados: "+str(x))
            tweet = tweets[i]
            row = dict(zip(['content', 'polarity', 'agreement'], [' '.join(list(tweet.itertext())), tweet.sentiment.get('polarity')]))
            row_s = pd.Series(row)
            row_s.name = i
            x+=1
            stompol_tweets_corpus_train = stompol_tweets_corpus_train.append(row_s)
        print("Registros tratados: "+str(x-1))
        stompol_tweets_corpus_train.to_csv('stompol-tweets-train-tagged.csv', index=False, encoding='utf-8')

    try:
        stompol_tweets_corpus_test = pd.read_csv(os.path.join(here,'stompol-tweets-test-tagged.csv'), encoding='utf-8')
    except:

        from lxml import objectify
        xml = objectify.parse(open(os.path.join(mypath,'stompol-test-tagged.xml')))
        
        root = xml.getroot()
        stompol_tweets_corpus_test = pd.DataFrame(columns=('content', 'polarity'))
        tweets = root.getchildren()
        print("Total de Registros: "+str(len(tweets)))
        x = 1
        for i in range(0,len(tweets)):
            if(x%5000 == 0): print("Registros tratados: "+str(x))
            tweet = tweets[i]
            row = dict(zip(['content', 'polarity', 'agreement'], [' '.join(list(tweet.itertext())), tweet.sentiment.get('polarity')]))
            row_s = pd.Series(row)
            row_s.name = i
            x+=1
            stompol_tweets_corpus_test = stompol_tweets_corpus_test.append(row_s)
        print("Registros tratados: "+str(x-1))
        stompol_tweets_corpus_test.to_csv('stompol-tweets-test-tagged.csv', index=False, encoding='utf-8')

    try:
        social_tweets_corpus_test = pd.read_csv(os.path.join(here,'socialtv-tweets-test-tagged.csv'), encoding='utf-8')
    except:

        from lxml import objectify
        xml = objectify.parse(open(os.path.join(mypath,'socialtv-test-tagged.xml')))
       
        root = xml.getroot()
        social_tweets_corpus_test = pd.DataFrame(columns=('content', 'polarity'))
        tweets = root.getchildren()
        print("Total de Registros: "+str(len(tweets)))
        x = 1
        for i in range(0,len(tweets)):
            if(x%5000 == 0): print("Registros tratados: "+str(x))
            tweet = tweets[i]
            row = dict(zip(['content', 'polarity', 'agreement'], [' '.join(list(tweet.itertext())), tweet.sentiment.get('polarity')]))
            row_s = pd.Series(row)
            row_s.name = i
            x+=1
            social_tweets_corpus_test = social_tweets_corpus_test.append(row_s)
        print("Registros tratados: "+str(x-1))        
        social_tweets_corpus_test.to_csv('socialtv-tweets-test-tagged.csv', index=False, encoding='utf-8')

    try:
        social_tweets_corpus_train = pd.read_csv(os.path.join(here,'socialtv-tweets-train-tagged.csv'), encoding='utf-8')
    except:
        from lxml import objectify
        xml = objectify.parse(open(os.path.join(mypath,'socialtv-train-tagged.xml')))
       
        root = xml.getroot()
        social_tweets_corpus_train = pd.DataFrame(columns=('content', 'polarity'))
        tweets = root.getchildren()
        print("Total de Registros: "+str(len(tweets)))
        x=1
        for i in range(0,len(tweets)):
            if(x%5000 == 0): print("Registros tratados: "+str(x))
            tweet = tweets[i]
            row = dict(zip(['content', 'polarity', 'agreement'], [' '.join(list(tweet.itertext())), tweet.sentiment.get('polarity')]))
            row_s = pd.Series(row)
            row_s.name = i
            x+=1
            social_tweets_corpus_train = social_tweets_corpus_train.append(row_s)
        print("Registros tratados: "+str(x-1))        
        social_tweets_corpus_train.to_csv('socialtv-tweets-train-tagged.csv', index=False, encoding='utf-8')    

    tweets_corpus = pd.concat([social_tweets_corpus_train,
                            social_tweets_corpus_test,
                            stompol_tweets_corpus_test,
                            stompol_tweets_corpus_train,
                            general_tweets_corpus_test,
                            general_tweets_corpus_train])    

    tweets_corpus = tweets_corpus.query('agreement != "DISAGREEMENT" and polarity != "NONE"')
    tweets_corpus = tweets_corpus[-tweets_corpus.content.str.contains('^http.*$')]

    
    ubic_datos = os.path.abspath(".")
    ubic_json = os.path.join(os.path.abspath("."),'scripts')
    ubic_db = os.path.join(ubic_datos, 'tweets.db')
    index_table = 1
    table = json.load(open(os.path.join(ubic_json,'tables.json')))[index_table]

    conn = createConnection(ubic_db)
    createTable(conn, table)

    num_regs = contar_regs(conn, table['name'])
    if num_regs == 0:

        campos = [x['name'] for x in table['fields']]
        campos.pop(campos.index('id'))
        campos = str(tuple(campos)).replace("'","")

        regs = []
        for _, row in tweets_corpus.iterrows():
            t = (row['content'],row['polarity'],row['agreement'])
            regs.append(t)

        insertar(conn, table['name'],campos, regs)

    return tweets_corpus


def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):

    stemmer = SnowballStemmer('spanish')    
    non_words = list(punctuation)
    non_words.extend(['¿', '¡'])
    non_words.extend(map(str,range(10)))


    # remove non letters
    text = ''.join([c for c in text if c not in non_words])
   
    tokens =  word_tokenize(text)


    try:
        stems = stem_tokens(tokens, stemmer)
    except Exception as e:
        print(e)
        print(text)
        stems = ['']
    return stems    


def modelization(tweets_corpus):

    nltk.download('stopwords')
    nltk.download('punkt')    
    spanish_stopwords = stopwords.words("spanish")
    spanish_stopwords = spanish_stopwords+['algun', 'com', 'contr', 'cuand', 'desd', 'dond', 'durant', 'eram', 'estab', 'estais', 'estam', 'estan', 'estand', 'estaran', 'estaras', 'esteis', 'estem', 'esten', 'estes', 'estuv', 'fuer', 'fues', 'fuim', 'fuist', 'hab', 'habr', 'habran', 'habras', 'hast', 'hem', 'hub', 'mas', 'mia', 'mias', 'mio', 'mios', 'much', 'nad', 'nosotr', 'nuestr', 'par', 'per', 'poc', 'porqu', 'qui', 'seais', 'seam', 'sent', 'ser', 'seran', 'seras', 'si', 'sient', 'sint', 'sobr', 'som', 'suy', 'tambien', 'tant', 'ten', 'tendr', 'tendran', 'tendras', 'teng', 'tien', 'tod', 'tuv', 'tuy', 'vosotr', 'vuestr','tambi']

    tweets_corpus = tweets_corpus[tweets_corpus.polarity != 'NEU']
    tweets_corpus['polarity_bin'] = 0
    tweets_corpus.polarity_bin[tweets_corpus.polarity.isin(['P', 'P+'])] = 1
    tweets_corpus.polarity_bin.value_counts(normalize=True)   
    vectorizer = CountVectorizer(
        analyzer='word',
        tokenizer= tokenize,
        lowercase=True,
        stop_words=spanish_stopwords
    ) 

    pipeline = Pipeline([
        ('vect', vectorizer),
        ('cls', LinearSVC()),
    ])



    parameters = {
        'vect__max_df': (0.5, 1.9),
        'vect__min_df': (10, 20,50),
        'vect__max_features': (500, 1000),
        'vect__ngram_range': ((1, 1), (1, 2)),  # unigrams or bigrams
        'cls__C': (0.2, 0.5, 0.7),
        'cls__loss': ('hinge', 'squared_hinge'),
        'cls__max_iter': (500, 1000)
    }


    grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1 , scoring='roc_auc')
    grid_search.fit(tweets_corpus.content, tweets_corpus.polarity_bin)  

    model = LinearSVC(C=.2, loss='squared_hinge',max_iter=1000,multi_class='ovr',
              random_state=None,
              penalty='l2',
              tol=0.0001
    )

    vectorizer = CountVectorizer(
        analyzer = 'word',
        tokenizer = tokenize,
        lowercase = True,
        stop_words = spanish_stopwords,
        min_df = 50,
        max_df = 1.9,
        ngram_range=(1, 1),
        max_features=1000
    )

    corpus_data_features = vectorizer.fit_transform(tweets_corpus.content)
    corpus_data_features_nd = corpus_data_features.toarray()

    scores = cross_val_score(
        model,
        corpus_data_features_nd[0:len(tweets_corpus)],
        y=tweets_corpus.polarity_bin,
        scoring='roc_auc',
        cv=5
    )

    print(scores.mean())
  

if __name__ == "__main__":
    from sqlite_ops import createConnection, createTable, contar_regs, insertar
    print(datetime.datetime.now())
    tweets_corpus = obtencionDatos()
    if (len(sys.argv) > 1 and sys.argv[1] == '--modelar'):        
        modelization(tweets_corpus)
    print(datetime.datetime.now())
