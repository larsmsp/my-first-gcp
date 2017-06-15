import os

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
from flask import Flask, request, jsonify
from peewee import *
from playhouse.flask_utils import FlaskDB

DATABASE = {
    'name': "tododb",
    'engine': "playhouse.pool.PooledPostgresqlDatabase",
    'user': "postgres",
    'password': "password"
}

ES_HOSTS_ENV = 'ELASTICSEARCH_HOSTS'
es_hosts = ['10.0.0.10:9200'] if ES_HOSTS_ENV not in os.environ else str(os.environ[ES_HOSTS_ENV]).split(',')

connections.create_connection(hosts=es_hosts)

app = Flask(__name__)
app.config.from_object(__name__)

db_wrapper = FlaskDB(app)
database = db_wrapper.database


class Task(db_wrapper.Model):
    created = DateTimeField()
    description = CharField()
    completed = BooleanField()

    class Meta:
        database = database


@app.route("/create", methods=['POST'])
def create():
    pass


@app.route("/complete/<int:item_id>", methods=['PUT'])
def complete(item_id):
    pass


@app.route("/search", methods=['GET'])
def search():
    query = request.args['query']
    results = Search(index='todo')\
        .highlight_options(require_field_match=False,
                           fragment_size=255,
                           pre_tags=['**'],
                           post_tags=['**'])\
        .highlight('description')\
        .query('query_string', query=query).execute()
    response = []
    for hit in results:
        response.append({
            'id': hit.meta.id,
            'description': hit.description,
            'completed': hit.completed,
            'highlight': list(hit.meta.highlight.contents)
        })
    return jsonify(response)


def main():
    database.create_tables([Task], safe=True)
    app.run()


if __name__ == '__main__':
    main()
