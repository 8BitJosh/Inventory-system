import sqlite3 as sql
from flask_restful import Resource

class All(Resource):
    def __init__(self, file):
        self.DBfile = file


    def get(self, format):
        conn = sql.connect(self.DBfile)
        c = conn.cursor()

        query = c.execute(
            '''SELECT * 
            FROM items
            ''')

        keys = ('id', 'name', 'store', 'location', 'other')
        
        if format in 'JSON':
            return {'data': [dict(zip(keys, i)) for i in query.fetchall()]}, 200

        if format in 'CSV':
            string = ','.join(keys) + '\n'

            for item in query.fetchall():
                string = string + ','.join(item) + '\n'

            return string

        return {'Error invalid format': format}