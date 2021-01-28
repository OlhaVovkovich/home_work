from datetime import datetime

import mongoengine as me

from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'flaskdb',
    'host': 'mongodb',
    'port': 27017,
}
db = MongoEngine(app)


class Visitor(me.Document):
    ipv4 = me.StringField(max_length=15, min_length=7)
    browser = me.StringField()
    created = me.DateTimeField(default=datetime.now)


@app.route('/')
def index():
    ipv4 = request.remote_addr
    browser = request.headers.get('User-Agent')

    visitors = []

    for visitor in Visitor.objects:
        visitor_dict = {}
        for field in ('ipv4', 'browser', 'created'):
            visitor_dict[field] = getattr(visitor, field)

        visitors.append(visitor_dict)

    visitor = Visitor(ipv4=ipv4, browser=browser)
    visitor.save()

    return jsonify(visitors)


if __name__ == '__main__':
    app.run()
