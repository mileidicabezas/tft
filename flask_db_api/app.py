from flask import Flask, redirect, url_for, render_template, jsonify, request
from flask_cors import CORS
import sqlite3 as s3
import simplejson as json
import os
from datetime import datetime
from datetime import timedelta
import calendar

app = Flask(__name__)
CORS(app)

ubic_db = os.path.join(os.path.abspath("."),"tweets.db")

@app.route("/api/tweets")
def return_tweets():
    conn = s3.connect(ubic_db)   
    str_select = '''select user, round(lat,3) lat, round(long,3) long, fec, trim(tweet) tweet, case when polarity = 0 then 'Negativo' else 'Positivo' end as polarity from tweets '''
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        l_reg = [r for r in reg]
        l_regs.append(l_reg)
    return jsonify(l_regs)

@app.route('/api/hashtags')
def return_hashtags():
    conn = s3.connect(ubic_db)   
    str_select = '''select UPPER(SUBSTR(hashtag, 1, 1)) || LOWER(SUBSTR(hashtag, 2)) hashtag, num from hashtags where hashtag !='Ninguno' order by num desc '''
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        l_reg = [r for r in reg]
        l_regs.append(l_reg)
    return jsonify(l_regs)

@app.route('/api/pie_data')    
def return_pie_data():
    str_inicio = '1970-01-01'
    str_fin = '3000-12-31'    
    
    conn = s3.connect(ubic_db)
    str_select = '''select sum(positivos) positivos, sum(negativos) negativos
                       from (select count('1') positivos ,0 negativos
                                from tweets where polarity = 1 
                                and date(fec) between '{INICIO}' and '{FIN}'
                             union select 0 positivos ,count('1') negativos
                                     from tweets
                                     where polarity = 0
                                     and date(fec) between '{INICIO}' and '{FIN}')'''.format(INICIO = str_inicio, FIN=str_fin)

    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)

@app.route('/api/pie_data_today')    
def return_pie_data_today():
    conn = s3.connect(ubic_db)
    str_select = '''select sum(positivos) positivos, sum(negativos) negativos
                       from (select count('1') positivos ,0 negativos
                                from tweets where polarity = 1 
                                and date(fec) = date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d'))
                             union select 0 positivos ,count('1') negativos
                                     from tweets
                                     where polarity = 0
                                     and date(fec) = date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d')))'''
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)


@app.route('/api/pie_porcentajes')
def return_porcentajes():
    str_inicio = '1970-01-01'
    str_fin = '3000-12-31'    

    
    conn = s3.connect(ubic_db)

    str_select = '''select round(sum(negativos),2)*100.0 negativos, round(sum(positivos),2)*100.0 positivos
                        from
                        (select count('1')*1.0/(select count('1') from tweets where date(fec) between '{INICIO}' AND '{FIN}') positivos, 0 negativos
                        from tweets
                        where polarity = 1
                            and date(fec)  between '{INICIO}' AND '{FIN}'
					 union
                        select 0 positivos, count('1')*1.0/(select count('1') from tweets where date(fec) between '{INICIO}' AND '{FIN}') negativos
                        from tweets
                        where polarity = 0
                            and date(fec) between '{INICIO}' AND '{FIN}')
							'''.format(INICIO=str_inicio, FIN=str_fin)

  
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)


@app.route('/api/pie_porcentajes_today')
def return_porcentajes_today():
    conn = s3.connect(ubic_db)
    str_select = '''select round(sum(negativos),2)*100.0 negativos, round(sum(positivos),2)*100.0 positivos
                        from
                        (select count('1')*1.0/(select count('1') from tweets where date(fec) like '%'||date('now')||'%') positivos, 0 negativos
                        from tweets
                        where polarity = 1
                            and date(fec) = date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d'))
                        union
                        select 0 positivos, count('1')*1.0/(select count('1') from tweets where date(fec) like '%'||date('now')||'%') negativos
                        from tweets
                        where polarity = 0
                            and date(fec) = date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d')))'''
  
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)


@app.route('/api/pie_data_yesterday')
def return_pie_data_yesterday():
    conn = s3.connect(ubic_db)
    str_select = '''select sum(positivos) positivos, sum(negativos) negativos
                       from (select count('1') positivos ,0 negativos
                                from tweets where polarity = 1 
                                and fec >= date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d'),'-1 day')
                             union select 0 positivos ,count('1') negativos
                                     from tweets
                                     where polarity = 0
                                     and fec >= date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d'),'-1 day'))'''
  
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)


@app.route('/api/pie_porcentajes_yesterday')
def return_porcentajes_yersterday():
    conn = s3.connect(ubic_db)
    str_select = '''select round(sum(negativos),2)*100.0 negativos, round(sum(positivos),2)*100.0 positivos
                        from
                        (select count('1')*1.0/(select count('1') from tweets where date(fec) >= date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d'),'-1 day')) positivos, 0 negativos
                        from tweets
                        where polarity = 1
                            and date(fec) >= date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d'),'-1 day')
                        union
                        select 0 positivos, count('1')*1.0/(select count('1') from tweets where date(fec) >= date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d'),'-1 day')) negativos
                        from tweets
                        where polarity = 0
                            and date(fec) >= date(strftime('%Y')||'-'||strftime('%m')||'-'||strftime('%d'),'-1 day'))'''
  
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)

@app.route('/api/pie_data_week')
def return_pie_data_week():
    fec_inicio = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)+timedelta(days=1)
    fec_fin = fec_inicio + timedelta(days=6)
    str_inicio = datetime.strftime(fec_inicio,'%Y-%m-%d')
    str_fin = datetime.strftime(fec_fin,'%Y-%m-%d')
    
    conn = s3.connect(ubic_db)
    str_select = '''select sum(positivos) positivos, sum(negativos) negativos
                       from (select count('1') positivos ,0 negativos
                                from tweets where polarity = 1 
                                and date(fec) between '{INICIO}' and '{FIN}'
                             union select 0 positivos ,count('1') negativos
                                     from tweets
                                     where polarity = 0
                                     and date(fec) between '{INICIO}' and '{FIN}')'''.format(INICIO = str_inicio, FIN=str_fin)


    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)


@app.route('/api/pie_porcentajes_week')
def return_porcentajes_week():
    conn = s3.connect(ubic_db)
    fec_inicio = datetime.today() - timedelta(days=datetime.today().isoweekday() % 7)+timedelta(days=1)
    fec_fin = fec_inicio + timedelta(days=6)
    str_inicio = datetime.strftime(fec_inicio,'%Y-%m-%d')
    str_fin = datetime.strftime(fec_fin,'%Y-%m-%d')

    str_select = '''select round(sum(negativos),2)*100.0 negativos, round(sum(positivos),2)*100.0 positivos
                        from
                        (select count('1')*1.0/(select count('1') from tweets where date(fec) between '{INICIO}' AND '{FIN}') positivos, 0 negativos
                        from tweets
                        where polarity = 1
                            and date(fec)  between '{INICIO}' AND '{FIN}'
					 union
                        select 0 positivos, count('1')*1.0/(select count('1') from tweets where date(fec) between '{INICIO}' AND '{FIN}') negativos
                        from tweets
                        where polarity = 0
                            and date(fec) between '{INICIO}' AND '{FIN}')
							'''.format(INICIO=str_inicio, FIN=str_fin)

  
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)

@app.route('/api/pie_data_month')
def return_pie_data_month():    
    today = datetime.now()
    mes = today.month
    anio = today.year
    rango = calendar.monthrange(anio, mes)
    str_inicio = str(today.year)+'-'+str(today.month)+'-'+'01'
    str_fin = str(today.year)+'-'+str(today.month)+'-'+str(rango[1])    
    
    conn = s3.connect(ubic_db)
    str_select = '''select sum(positivos) positivos, sum(negativos) negativos
                       from (select count('1') positivos ,0 negativos
                                from tweets where polarity = 1 
                                and date(fec) between '{INICIO}' and '{FIN}'
                             union select 0 positivos ,count('1') negativos
                                     from tweets
                                     where polarity = 0
                                     and date(fec) between '{INICIO}' and '{FIN}')'''.format(INICIO = str_inicio, FIN=str_fin)

    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)



@app.route('/api/pie_porcentajes_month')
def return_porcentajes_month():
    today = datetime.now()
    mes = today.month
    anio = today.year
    rango = calendar.monthrange(anio, mes)
    str_inicio = str(today.year)+'-'+str(today.month)+'-'+'01'
    str_fin = str(today.year)+'-'+str(today.month)+'-'+str(rango[1])    
    
    conn = s3.connect(ubic_db)

    str_select = '''select round(sum(negativos),2)*100.0 negativos, round(sum(positivos),2)*100.0 positivos
                        from
                        (select count('1')*1.0/(select count('1') from tweets where date(fec) between '{INICIO}' AND '{FIN}') positivos, 0 negativos
                        from tweets
                        where polarity = 1
                            and date(fec)  between '{INICIO}' AND '{FIN}'
					 union
                        select 0 positivos, count('1')*1.0/(select count('1') from tweets where date(fec) between '{INICIO}' AND '{FIN}') negativos
                        from tweets
                        where polarity = 0
                            and date(fec) between '{INICIO}' AND '{FIN}')
							'''.format(INICIO=str_inicio, FIN=str_fin)

  
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)

@app.route('/api/pie_data_year')
def return_pie_data_year():    
    today = datetime.now()
    str_inicio = str(today.year)+'-01-01'
    str_fin = str(today.year)+'-12-31'    
    
    conn = s3.connect(ubic_db)
    str_select = '''select sum(positivos) positivos, sum(negativos) negativos
                       from (select count('1') positivos ,0 negativos
                                from tweets where polarity = 1 
                                and date(fec) between '{INICIO}' and '{FIN}'
                             union select 0 positivos ,count('1') negativos
                                     from tweets
                                     where polarity = 0
                                     and date(fec) between '{INICIO}' and '{FIN}')'''.format(INICIO = str_inicio, FIN=str_fin)

    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)

@app.route('/api/pie_porcentajes_year')
def return_porcentajes_year():
    today = datetime.now()
    str_inicio = str(today.year)+'-01-01'
    str_fin = str(today.year)+'-12-31'    
    
    conn = s3.connect(ubic_db)

    str_select = '''select round(sum(negativos),2)*100.0 negativos, round(sum(positivos),2)*100.0 positivos
                        from
                        (select count('1')*1.0/(select count('1') from tweets where date(fec) between '{INICIO}' AND '{FIN}') positivos, 0 negativos
                        from tweets
                        where polarity = 1
                            and date(fec)  between '{INICIO}' AND '{FIN}'
					 union
                        select 0 positivos, count('1')*1.0/(select count('1') from tweets where date(fec) between '{INICIO}' AND '{FIN}') negativos
                        from tweets
                        where polarity = 0
                            and date(fec) between '{INICIO}' AND '{FIN}')
							'''.format(INICIO=str_inicio, FIN=str_fin)

  
    cur = conn.cursor()
    cur.execute(str_select)
    l_regs = []
    regs = cur.fetchall()
    for reg in regs:
        for r in reg:
            l_regs.append(r)
    return jsonify(l_regs)

@app.route('/api/desglose')
def return_desglose():
    conn = s3.connect(ubic_db)
    l_regs = []
    hashtag = request.args.get('hashtag')    
    str_select = '''select tw.user, 
                    round(tw.lat,3) lat, 
                    round(tw.long,3) long, 
                    tw.fec, 
                    trim(tw.tweet) tweet, 
                    case when tw.polarity = 0 then 'Negativo' else 'Positivo' end as polarity 
                    from hashtags_tweets htw,
                        tweets tw
                    where htw.tweet_id = tw.id
                      and lower(htw.hashtag) = lower({HASHTAG}) '''.format(HASHTAG=hashtag)

    cur = conn.cursor()
    cur.execute(str_select)
    regs = cur.fetchall()
    for reg in regs:
        l_reg = [r for r in reg]
        for lr in l_reg:
            if isinstance(lr,str):
                lr = lr.replace("[","").replace("]","").replace('|','').replace('\n','')
        l_regs.append(l_reg)
    my_json = jsonify(l_regs)
    return my_json

@app.route('/api/weeks')
def return_weeks():
    l_dates = []
    l_meses = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    #month_range = calendar.monthrange(datetime.today().year, datetime.today().month)
    month_range = calendar.monthrange(datetime.today().year-1, 11)
    #first_day = '01/{MES}/{ANIO}'.format(MES=datetime.today().month, ANIO=datetime.today().year)
    first_day = '01/{MES}/{ANIO}'.format(MES=11, ANIO=datetime.today().year-1)
    #last_day = str(month_range[1])+'/{MES}/{ANIO}'.format(MES=datetime.today().month, ANIO=datetime.today().year)
    last_day = str(month_range[1])+'/{MES}/{ANIO}'.format(MES=11, ANIO=datetime.today().year-1)
    last_day_month = datetime.strptime(last_day, '%d/%m/%Y')    
    first_week_1_day = datetime.strptime(first_day, '%d/%m/%Y')    
    first_week_last_day = first_week_1_day+timedelta(days=7-month_range[0]-1) 
    l_dates.append((first_week_1_day, first_week_last_day))    
    salir = False

    ini_day_week = first_week_last_day+timedelta(days=1)
    while(not salir):
        last_day_week = ini_day_week+timedelta(days=6)
        if last_day_week >= last_day_month:
            l_dates.append((ini_day_week,last_day_month))
            salir = True
        else:
            l_dates.append((ini_day_week, last_day_week))
            print(last_day_week)
            ini_day_week = last_day_week+timedelta(days=1)

    
    l_hashtags_results = []
    l_titulos = []
    l_selects = []
    for dates in l_dates:
        date_ini = dates[0]
        date_fin = dates[1]
        fec_ini = '{ANIO}-{MES}-{DIA}'.format(ANIO=str(date_ini.year),MES=str(date_ini.month).zfill(2),DIA=str(date_ini.day).zfill(2))
        fec_fin = '{ANIO}-{MES}-{DIA}'.format(ANIO=str(date_fin.year),MES=str(date_fin.month).zfill(2),DIA=str(date_fin.day).zfill(2))
        str_select = '''select htw.hashtag, count('1') num_regs
                            from hashtags_tweets htw,
                                 tweets twt
                        where twt.id = htw.tweet_id
                            and date(fec) between '{FEC_INI}' and '{FEC_FIN}'
                            and htw.hashtag != 'Ninguno'
                            group by htw.hashtag
                            order by 2 desc '''.format(FEC_INI=fec_ini, FEC_FIN=fec_fin)

        titulo = 'Semana del {DIA}-{MES}-{ANIO} al {DIAF}-{MES}-{ANIO}'.format(ANIO=str(date_ini.year),MES=str(date_ini.month).zfill(2),DIA=str(date_ini.day).zfill(2),DIAF=str(date_fin.day).zfill(2))
        l_titulos.append(titulo)
        conn = s3.connect(ubic_db)
        cur = conn.cursor()
        cur.execute(str_select)
        l_selects.append(str_select)
        regs = cur.fetchall()
        l_hashtags = []
        for reg in regs:
            dict_reg = {}
            dict_reg[reg[0]] = reg[1]
            l_hashtags.append(dict_reg)
        l_hashtags_results.append(l_hashtags)

    dict_rdo = {}
    dict_rdo['anio'] = date_ini.year
    dict_rdo['mes'] = l_meses[date_ini.month-1]
    dict_rdo['fechas'] = l_dates
    dict_rdo['registros'] = l_hashtags_results    
    dict_rdo['titulos'] = l_titulos
    return jsonify(dict_rdo)
    





if __name__ == "__main__":
    app.run(debug=True,port=5005)