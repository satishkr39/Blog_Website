# carcompanyblog/__init__.py file
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager


app =Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'mysecretkey'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app, db)

# setup login maanger

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

from carcompanyblog.core.views import core
from carcompanyblog.error_pages.handler_views import error_pages
from carcompanyblog.users.views import users
from carcompanyblog.blog_post.views import blog_posts
app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(blog_posts)
