import sqlite3

class DB:
    def __enter__(self):
        self.con = sqlite3.connect('base.db')
        self. cur = self.con.cursor()
        return self
        
    def select_info(self, table_name, columns='*', conditions=None):
        qry = 'SELECT %s FROM %s' % (columns, table_name)
        if conditions:
            qry = 'SELECT %s FROM %s WHERE %s' % (columns, table_name, conditions)
        self.cur.execute(qry)
        result = self.cur.fetchall()
        return result

    def insert_info(self, table_name, data):
        columns = ', '.join(data.keys())
        placeholders = ':' + ', :'.join(data.keys())
        qry = 'INSERT INTO %s (%s) VALUES (%s)' % (table_name, columns, placeholders)
        self.cur.execute(qry, data)
        self.con.commit()

    def update_info(self, table_name, data, conditions):
        set_lines = ",".join([f"{k}=:{k}" for k in data.keys()])
        qry = 'UPDATE %s SET %s WHERE %s' % (table_name, set_lines, conditions)
        self.cur.execute(qry, data)
        self.con.commit()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.con.close()

