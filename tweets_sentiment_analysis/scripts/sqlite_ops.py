import sqlite3 as sq3
'''from flask_sqlalchemy import SQLAlchemy    ------  sq3 = SQLAlchemy()'''
import psycopg2  
import re

def createConnection(db_file):
    conn = None
    try:
        conn = sq3.connect(db_file)
    except sq3.Error as err:
        print(err)
    
    return conn

def createTable(conn, table):    
    string_create = 'CREATE TABLE IF NOT EXISTS {NOMBRE} ({CAMPOS})'
    nombre = table['name']
    str_fields = ""
    

    for field in table['fields']:

        str_field = "{FIELD_NAME} {FIELD_TYPE} {OTHERS},"
        str_required = "{REQUIRED}"
        str_primary = "{PK}"
        str_auto_inc = "{AINC}"

        
        if 'required' in field:
            str_required = str_required.format(REQUIRED=' NOT NULL ')
        else:
            str_required = str_required.format(REQUIRED='')

        if 'primary' in field:
            str_primary = str_primary.format(PK=' PRIMARY KEY ')
        else:
            str_primary = str_primary.format(PK='')

        if 'auto_increment' in field:
            str_auto_inc = str_auto_inc.format(AINC=' AUTOINCREMENT ')
        else:
            str_auto_inc = str_auto_inc.format(AINC='')

        str_field = str_field.format(FIELD_NAME=field['name'],FIELD_TYPE=field['type'],OTHERS=str_required+str_primary+str_auto_inc)
        str_fields+=str_field

    str_fields = str_fields[0:len(str_fields)-2]
    string_create = string_create.format(NOMBRE=nombre, CAMPOS=str_fields)
    string_create = re.sub('  ',' ',string_create).lower()
    conn.execute(string_create)

def insertar(conn, table, fields, regs):
    str_insert = '''INSERT INTO {TABLE} {FIELDS} VALUES ('''.format(TABLE=table,FIELDS=fields)
    for rn in range(0, len(regs[0])):
        str_insert+='?,'
    str_insert=str_insert[0:len(str_insert)-1]+')'
    conn.executemany(str_insert,regs)
    conn.commit()

def contar_regs(conn, table):
    str_select = '''SELECT COUNT('1') FROM {TABLE}'''.format(TABLE=table)
    cur = conn.cursor()
    cur.execute(str_select)
    rows = cur.fetchone()
    return rows[0]

def truncar(conn, table):
    str_truncate = '''DELETE FROM {TABLE}'''.format(TABLE=table)
    cur = conn.cursor()
    cur.execute(str_truncate)
    conn.commit()

def cerrar(conn):
    conn.execute('VACUUM')
    conn.close()