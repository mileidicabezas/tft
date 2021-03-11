# coding=utf-8
from flask import Flask, redirect, url_for, render_template, jsonify, request
import requests
import simplejson as json
import colorsys
import random
import datetime

app = Flask(__name__)
    

@app.route("/")
def home():    
    dict_titulo = {"titulo":"Análisis de sentimientos sobre tendencias en Twitter","descripcion":"Twitter es una de las plataformas mas utilizadas para la expresión de opiniones e ideas, es por esta razón que es una de las mejores fuentes de la cual extraer estadísticas sociales. En este proyecto se pretende analizar la información extraída de twitter centrándose en el análisis de polaridad, es decir se busca establecer la subjetividad de las opiniones expresadas por los usuarios de esta plataforma. Esta aplicación muestra y analizan los resultados obtenidos por el proceso de obtención de datos y análisis de sentimientos de los tweets en las diferentes zonas de Ecuador."}
    opciones = [{
        'titulo':'Geolocalización de tweets',
        'descripcion':'Tweets geolocalizados en Quito y su ubicación en el mapa.',
        'imagen':'images/maplocation.jpg',
        'url_destino':'/mapas'
    },
    {
        'titulo':'Analisis de tendencias',
        'descripcion':'Analisis de los terminos mas utilizados en Twitter',
        'imagen':'images/trends6.jpg',
        'url_destino':'/tendencias'
    }]
    return render_template("index.html", opciones=opciones, home_activator="active", cabecera=dict_titulo)

def limpiar_resultados(p_string):
    return p_string.replace('[','').replace(']','').replace('\n','').split(', ')

@app.route("/mapas")
def mapas():
    d = requests.get('http://localhost:5005/api/pie_data')
    p = requests.get('http://localhost:5005/api/pie_porcentajes')
    d_today = requests.get('http://localhost:5005/api/pie_data_today')
    p_today = requests.get('http://localhost:5005/api/pie_porcentajes_today')
    d_yesterday = requests.get('http://localhost:5005/api/pie_data_yesterday')
    p_yesterday = requests.get('http://localhost:5005/api/pie_porcentajes_yesterday')
    d_week = requests.get('http://localhost:5005/api/pie_data_week')
    p_week = requests.get('http://localhost:5005/api/pie_porcentajes_week')
    d_month = requests.get('http://localhost:5005/api/pie_data_month')
    p_month = requests.get('http://localhost:5005/api/pie_porcentajes_month')
    d_year = requests.get('http://localhost:5005/api/pie_data_year')
    p_year = requests.get('http://localhost:5005/api/pie_porcentajes_year')

    dt = d.text.replace('[','').replace(']','').replace('\n','').split(', ')
    dt_today = d_today.text.replace('[','').replace(']','').replace('\n','').split(', ')
    dt_yesterday = d_yesterday.text.replace('[','').replace(']','').replace('\n','').split(', ')
    dt_week = d_week.text.replace('[','').replace(']','').replace('\n','').split(', ')
    dt_month = d_month.text.replace('[','').replace(']','').replace('\n','').split(', ')
    dt_year = d_year.text.replace('[','').replace(']','').replace('\n','').split(', ')

    pt = p.text.replace('[','').replace(']','').replace('\n','').split(', ')
    pt_today = p_today.text.replace('[','').replace(']','').replace('\n','').split(', ')
    pt_yesterday = p_yesterday.text.replace('[','').replace(']','').replace('\n','').split(', ')
    pt_week = p_week.text.replace('[','').replace(']','').replace('\n','').split(', ')
    pt_month = p_month.text.replace('[','').replace(']','').replace('\n','').split(', ')
    pt_year = p_year.text.replace('[','').replace(']','').replace('\n','').split(', ')


    dict_datos = {
        'titulo':'Visualización de sentimientos de los tweets',
        'descripcion':'En este apartado se muestran los su contenido de los tweets y la polaridad sujeta a cada tweet en base al análisis de sentimiento realizado, tambien se puden vizualizar graficas semanalas de la evolución del los sentimientos en base a las tendencias.',
        'imagen':'static/images/quito_tweets.png',
        'tabs':{
            'tab1_name':'Concentración de los tweets',
            'tab1_map_description':"La geolocalización de los tweets permite obtener la ubicación de los usuarios activos en Twitter, aqui se muestran las localización de los tweets publicados con el contenido del tweets y la polaridad correspondiente.",
            'tab2_name':'Tweets & Análisis de Sentimientos',
            'tab2_description':'En la siguiente tabla se muestran tanto los tweets como su polaridad positiva o negativa correspondiete a cada tweet.',
            'tab3_name':'Graficos',
            'tab3_description':'Gráficos de sentimientos de los tweets según el periodo temporal'
        },
        "labels": ["Positivo"+pt[1]+'%' ,"Negativo"+pt[0]+'%'],
        "labels_today":["Positivo"+pt_today[1]+'%' ,"Negativo"+pt_today[0]+'%'],
        "labels_yesterday":["Positivo"+pt_yesterday[1]+'%' ,"Negativo"+pt_yesterday[0]+'%'],
        "labels_week":["Positivo"+pt_week[1]+'%' ,"Negativo"+pt_week[0]+'%'],
        "labels_month":["Positivo"+pt_month[1]+'%' ,"Negativo"+pt_month[0]+'%'],
        "labels_year":["Positivo"+pt_year[1]+'%' ,"Negativo"+pt_year[0]+'%'],
        "valores":[int(x) for x in dt],
        "valores_today":[int(x) for x in dt_today],
        "valores_yesterday":[int(x) for x in dt_yesterday],
        "valores_week":[int(x) for x in dt_week],
        "valores_month":[int(x) for x in dt_month],
        "valores_year":[int(x) for x in dt_year],
        "colors" : ["#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1","#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
     
    }

    my_set=zip(dict_datos['valores'], 
               dict_datos['labels'], 
               dict_datos['colors'],
               dict_datos['valores_today'],
               dict_datos['labels_today'],
               dict_datos['valores_yesterday'],
               dict_datos['labels_yesterday'],
               dict_datos['valores_week'],
               dict_datos['labels_week'],
               dict_datos['valores_month'],
               dict_datos['labels_month'],
               dict_datos['valores_year'],
               dict_datos['labels_year']               )

    return render_template("mapas.html",geo_activator="active",datos=dict_datos, set=my_set)

@app.route('/tendencias')
def tendencias():
    d = requests.get('http://localhost:5005/api/hashtags')
    dt = d.json()

    d2 = requests.get('http://localhost:5005/api/weeks')
    dt2 = d2.json()

    l_labels = []
    l_datos = []
    for reg in dt2['registros']:
        l_etiq = []
        l_dat = []
        for r in reg:
            k = list(r.keys())[0]
            v = r[k]
            l_etiq.append(k)
            l_dat.append(v)
        l_labels.append(l_etiq)
        l_datos.append(l_dat)


    
    N = 150
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    l_colors = []
    l_hex = []
    levels = range(32,256,32)
    for rng in range(0,2000):
        l_colors.append(tuple(random.choice(levels) for _ in range(3)))
    
    l_hex = ['#%02x%02x%02x'.upper()%x for x in l_colors]
    
    p = requests.get('http://localhost:5005/api/pie_porcentajes')
    pt = p.text.replace('[','').replace(']','').replace('\n','').split(', ')
    dict_datos = {
        'titulo':'Análisis de Tendencias',
        'descripcion':'En este apartado se muestran los hashtags que son tendencia.',
        'imagen':'static/images/hashtags.png',
        'tabs':{
            'tab1_name':'Nube de Palabras',
            'tab1_map_description':"Los hashtags que son tendencia en Quito. Cuanto más tendencia sea un hashtag, mayor será el tamaño de su fuente",
            'tab2_name':'Hashtags',
            'tab2_description':'Tabla con los diferentes hashtags de los tweets geolocalizados.',
            'tab3_name':'Graficos',
            'tab3_description':'Graficos de barras representando la frecuencia de los diferentes hashtags'
        },
        "labels": [x[0].replace('[','').replace('@','').replace('\n','') for x in dt],
        "valores":[x[1]for x in dt],
        "colors" : l_hex,
        "weeks":{"datos":dt2,
                 "len_fechas":len(dt2['fechas']),
                 "labels0":l_labels[0],
                 "values0":l_datos[0],
                 "labels1":l_labels[1],
                 "values1":l_datos[1],
                 "labels2":l_labels[2],
                 "values2":l_datos[2],
                 "labels3":l_labels[3],
                 "values3":l_datos[3],
                 "labels4":l_labels[4],
                 "values4":l_datos[4]

                 }
       
    }
    my_set=zip(dict_datos['valores'], dict_datos['labels'], dict_datos['colors'])
    return render_template("tendencias.html",trends_activator="active", datos=dict_datos, set=my_set)

@app.route('/desglose')
def desglose():
        #p = requests.get('http://localhost:5005/api/tweets')
        dict_datos = {
        'titulo' : 'Tweets con el hashtag "'+request.args['hashtag']+'"',
        'hashtag':request.args['hashtag'],
        'tabs':{
            'titulo1':'Tabla de Tweets'
            }
        }
        return render_template("mapas1.html",datos=dict_datos)


if __name__ == "__main__":
    app.run(debug=True)
