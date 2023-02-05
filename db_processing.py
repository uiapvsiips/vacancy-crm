import sqlite3

def select_info(table_name, columns='*', conditions=None):
    qry = 'SELECT %s FROM %s' % (columns, table_name)
    if conditions:
        qry = 'SELECT %s FROM %s WHERE %s' % (columns, table_name, conditions)
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    cur.execute(qry)
    result = cur.fetchall()
    cur.close()
    con.close()
    return result

def insert_info(table_name, data):
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    columns = ', '.join(data.keys())
    placeholders = ':' + ', :'.join(data.keys())
    qry = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, columns, placeholders)
    cur.execute(qry, data)
    cur.close()
    con.commit()
    con.close()

def update_info(table_name, data, conditions):
    con = sqlite3.connect('base.db')
    cur = con.cursor()
    set_lines = ",".join([f"{k}=:{k}" for k in data.keys()])
    qry = 'UPDATE %s SET %s WHERE %s' % (table_name, set_lines, conditions)
    cur.execute(qry, data)
    cur.close()
    con.commit()
    con.close()

