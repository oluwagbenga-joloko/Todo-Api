from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate

from .models import db
from .resources.todos import TodoListResource, TodoResource
from .resources.users import UserListResource, AuthResource, UserResource
from .resources.todo_items import TodoItemListResource, TodoItemResource
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

    api.add_resource(TodoListResource, "/api/todos")
    api.add_resource(TodoResource, "/api/todos/<int:todo_id>")
    api.add_resource(UserListResource, "/api/users")
    api.add_resource(UserResource, "/api/users/<int:user_id>")
    api.add_resource(AuthResource, '/api/users/login')
    api.add_resource(TodoItemListResource, '/api/todos/<int:todo_id>/todo_items')
    api.add_resource(TodoItemResource, '/api/todos/<int:todo_id>/todo_items/<int:todo_item_id>')

    return app



