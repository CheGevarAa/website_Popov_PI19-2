from blog import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(64), nullable=False, default='default2.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy=True)
    tickets = db.relationship('Ticket', backref='owner', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username {self.username}"


class Post(db.Model):
    users = db.relationship(User)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID {self.id} -- Date {self.date} -- {self.title}"


class Ticket(db.Model):
    user = db.relationship(User)
    ticket_id = db.Column(db.Integer, primary_key=True)
    departure_time = db.Column(db.String(64), nullable=False)
    arrival_time = db.Column(db.String(64), nullable=False)
    simple = db.Column(db.Integer, nullable=False)
    high_class = db.Column(db.Integer, nullable=False)
    day = db.Column(db.DateTime, nullable=False)
    departure_point = db.Column(db.String(64), nullable=False)
    arrival_point = db.Column(db.String(64), nullable=False)
    simple_price = db.Column(db.Integer, nullable=False)
    high_price = db.Column(db.Integer, nullable=False)

    def __init__(self, simple, high_class, day, departure_time, arrival_time, departure_point, arrival_point,
                 simple_price, high_price):
        self.simple = simple
        self.arrival_time = arrival_time
        self.departure_time = departure_time
        self.high_class = high_class
        self.day = day
        self.departure_point = departure_point
        self.departure_point = arrival_point
        self.simple_price = simple_price
        self.high_class = high_price
