import sqlite3 as sql

from flask import Flask, render_template
from flask_restful import Api

from All_endpoint import All
from Single_endpoint import Single
from Search_endpoint import Search
from ID_endpoint import ID

DBfile = 'database.db'

conn = sql.connect(DBfile)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS items(
        id TEXT PRIMARY KEY,
        name TEXT,
        store TEXT,
        location TEXT,
        other TEXT
    )''')

conn.commit()

app = Flask(__name__)
api=Api(app)


@app.route('/')
def index():
    return render_template('index.html')


api.add_resource(All, '/api/all/<format>', resource_class_args=(DBfile,))
api.add_resource(Single, '/api/single/<id>', resource_class_args=(DBfile,))
api.add_resource(Search, '/api/search', resource_class_args=(DBfile,))
api.add_resource(ID, '/api/ID', resource_class_args=(DBfile,))

app.run(host='0.0.0.0', port=80, debug=True)
