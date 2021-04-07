import datetime
import uuid

from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from werkzeug.wrappers import Request, Response


app = Flask(__name__)
api = Api(app=app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(), unique=True, nullable=False)
    time_create = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def is_expired(self):
        return datetime.datetime.utcnow() > self.time_create + datetime.timedelta(days=1)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(6), nullable=False)
    telephone = db.Column(db.String(13), unique=True, nullable=False)
    token = db.relationship('Token', uselist=False)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    room_id = db.Column(db.Integer)
    settlement_date = db.Column(db.Date)
    user_info = db.relationship('User', backref='pet')


class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(30))
    time = db.Column(db.String(30))
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    creation_time = db.Column(db.String(255))
    product_id = db.Column(db.Integer)


class OrderLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    price = db.Column(db.Float)


class OurMiddleware:
    NOT_AUTH = {'/register', '/login'}

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):

        request = Request(environ)

        if request.path in self.NOT_AUTH:
            return self.app(environ, start_response)

        token = db.session.query(Token). \
            filter(Token.token == request.headers.get('authorization')). \
            scalar()

        if token is None or token.is_expired():
            res = Response('Wrong api_token', mimetype='text/plain', status=401)
            return res(environ, start_response)

        environ['user'] = token.user_id
        return self.app(environ, start_response)


app.wsgi_app = OurMiddleware(app.wsgi_app)


class Login(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        user = db.session.query(User). \
            filter(User.username == username). \
            filter(User.password == password). \
            scalar()

        if user is None:
            abort(404)

        user.token.token = str(uuid.uuid4())
        user.token.time_create = datetime.datetime.utcnow()
        db.session.commit()

        return {'token': user.token.token}


class Register(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        telephone = request.json.get('telephone')
        if username is None or password is None or telephone is None:
            abort(400)  # missing arguments

        user = User(username=username, password=password, telephone=telephone)
        db.session.add(user)
        db.session.flush()

        token = Token(token=str(uuid.uuid4()), user_id=user.id)
        db.session.add(token)

        db.session.commit()

        return {'token': token.token}


api.add_resource(Login, '/login')
api.add_resource(Register, '/signup')


class Order(Resource):
    def get(self):
        orders = Order.query.filter_by(user_id=request.environ['user'].id).all()

        if orders:
            response = {}
            for i in orders:
                response['order_%s' % i.id] = {
                    'creation_time': i.creation_time,
                    'product_id': i.product_id
                }
            return {"orders": response}
        else:
            return {'error': 'order is empty'}, 404

    def post(self):
        from datetime import datetime
        response = request.get_json()
        product_id = response['product_id']
        creation_time = '%s' % datetime.now()

        order = Order(user_id=current_user.id,
                      creation_time=creation_time,
                      product_id=product_id)

        db.session.add(order)
        db.session.commit()

        return {"status": "success"}


api.add_resource(Order, '/order')


if __name__ == '__main__':
    app.run(debug=True)
