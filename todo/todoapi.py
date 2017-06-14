from flask import Flask
from peewee import *
from playhouse.flask_utils import FlaskDB

DATABASE = {
    'name': "tododb",
    'engine': "playhouse.pool.PooledPostgresqlDatabase",
    'user': "postgres",
    'password': "password"
}


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


@app.route("/complete/<int:item_id>", methods=["PUT"])
def complete(item_id):
    pass


def main():
    database.create_tables([Task], safe=True)
    app.run()


if __name__ == '__main__':
    main()
