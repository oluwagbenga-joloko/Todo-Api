from flask_restful import Resource
from flask import request, jsonify, g
from marshmallow import ValidationError
from ..models import Todo , todo_schema, todos_schema
from ..util import validate_request, jwt_required


class TodoListResource(Resource):

    @validate_request
    @jwt_required
    def post(self):
        payload = request.get_json()
        try:
            todo_schema.load(payload)
        except ValidationError as err:
            return err.messages, 400

        todo = Todo(title=payload["title"], user_id=g.current_user["id"])
        todo.save()
        return {"message": "todo created", "todo": todo_schema.dump(todo)}, 201
    
    @jwt_required
    def get(self):
        todos = Todo.query.filter_by(user_id=g.current_user["id"])
        todos_schema.dump(todos)
        return {"message": "todos retrieved", "todos": todos_schema.dump(todos)}, 200


class TodoResource(Resource):

    @jwt_required
    def get(self, todo_id):
        user_id = g.current_user["id"]
        todo = Todo.query.get(todo_id)
        if not todo:
            return {"message": "todo does not exist"}, 404

        if todo.user_id != user_id:
            return {"message": "unauthorized"}, 401
        
        return {"message": "todo retrieved", "todo": todo_schema.dump(todo)}, 200
    
    @jwt_required
    def delete(self, todo_id):
        user_id = g.current_user["id"]
        todo = Todo.query.get(todo_id)
        if not todo:
            return {"message": "todo does not exist"}, 404

        if todo.user_id != user_id:
            return {"message": "unauthorized"}, 401

        todo.delete()
        return {"message": "todo deleted"} , 200
    
    @validate_request
    @jwt_required
    def put(self, todo_id):
        payload = request.get_json()
        user_id = g.current_user["id"]
        todo = Todo.query.get(todo_id)
        if not todo:
            return {"message": "todo does not exist"}, 404

        if todo.user_id != user_id:
            return {"message": "unauthorized"}, 401  

        try:
            todo_schema.load(payload)
        except ValidationError as err:
            return err.messages, 400
        
        todo.title = payload["title"]
        todo.save()
        return {"message": "todo updated", "todo": todo_schema.dump(todo)}, 200
            