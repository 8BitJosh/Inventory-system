import sqlite3 as sql

from flask_restful import Resource
from random import randrange

class ID(Resource):
    def __init__(self, file):
        self.DBfile = file


    def get(self):
        used = True
        ID = ''

        conn = sql.connect(self.DBfile)
        c = conn.cursor()

        while used:
            num = []
            for i in range(0,4):
                num.append( str(randrange(64)).zfill(2) )

            ID = ':'.join(num)

            query = c.execute(
                '''SELECT * FROM items
                WHERE id = ?''',
                (ID,))

            used = len(query.fetchall()) is not 0

        print(ID)
        return {'id': ID}