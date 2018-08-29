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
            SELECT id, name, store, location FROM items
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

            q = 'SELECT id, name, store, location FROM items WHERE id in (' + ",".join(['?']*len(results)) + ')'
            query = c.execute(q, ids)

        data = []

        for item in query.fetchall():
            x = {}
            x['id'] = item[0]
            x['name'] = item[1]

            if item[3] not in '':
                x['loc'] = item[3]
            else:
                x['loc'] = item[2]  

            data.append(x)

        return {'data': data}, 200
