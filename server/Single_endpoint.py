import sqlite3 as sql

from flask import request
from flask_restful import Resource


class Single(Resource):
    def __init__(self, file):
        self.DBfile = file


    def get(self, id):
        conn = sql.connect(self.DBfile)
        c = conn.cursor()

        query = c.execute(
            '''SELECT * 
            FROM items
            WHERE id = ?
            ''', (id,))

        data = query.fetchone()

        if data is None:
            return {'Info': 'ID does not exist'}

        keys = ('id', 'name', 'store', 'location', 'other')

        return dict(zip(keys, data)), 200

    def post(self, id):
        req = {k:v for k,v in request.form.items()}

        conn = sql.connect(self.DBfile)
        c = conn.cursor()

        c.execute(
            '''INSERT OR REPLACE INTO items
            (id, name, store, location, other)
            VALUES (?,?,?,?,?)
            ''', (
                req['id'],
                req['name'],
                req['store'],
                req['location'],
                req['other']
                ))

        conn.commit()

        return {'Info': 'Success'}


    def delete(self, id):
        conn = sql.connect(self.DBfile)
        c = conn.cursor()

        c.execute(
            '''
            DELETE FROM items
            WHERE id = ?
            ''', 
            (id,))

        conn.commit()

        return {'id': id}