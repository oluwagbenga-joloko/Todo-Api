from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from .models import db
from .resources.todos import TodoList
from config import app_config
import os


def create_flask_app(environment):
    app = Flask(__name__)
    app.config.from_object(app_config[environment])
    db.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app)
   
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    api.add_resource(TodoList, "/api/todos")
    
    return app



