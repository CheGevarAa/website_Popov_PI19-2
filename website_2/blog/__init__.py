import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ushallnotpass'

app.config.from_pyfile('config.cfg')

mail = Mail(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

from blog.base.views import base
from blog.blog_posts.veiws import blog_posts
from blog.users.veiws import users
from blog.stock.veiws import stock
from blog.errors.handlers import errors


app.register_blueprint(base)
app.register_blueprint(blog_posts)
app.register_blueprint(users)
app.register_blueprint(stock)
app.register_blueprint(errors)

