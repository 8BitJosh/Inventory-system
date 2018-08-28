import sqlite3 as sql

from flask import request
from flask_restful import Resource

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class Search(Resource):
    def __init__(self, file):
        self.DBfile = file


    def get(self):
        # req = request.get_json()
        search = request.args.get('query', default='')

        keys = ('id', 'name')

        conn = sql.connect(self.DBfile)
        c = conn.cursor()

        query = c.execute(
            '''
            SELECT id, name FROM items
            ''')

        if search not in '':
            items = {}

            for item in query.fetchall():
                items[item[0]] = item[1]

            results = process.extractBests(search, 
                items, scorer=fuzz.token_sort_ratio, limit=10, score_cutoff=20)

            ids = []
            for result in results:
                ids.append(result[2])

            q = 'SELECT id, name FROM items WHERE id in (' + ",".join(['?']*len(results)) + ')'
            query = c.execute(q, ids)


        return {'data': [dict(zip(keys, i)) for i in query.fetchall()]}, 200
