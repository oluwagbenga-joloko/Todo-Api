from flask_restful import Resource
from flask import request, jsonify
from marshmallow import ValidationError
from ..models import Todo , todo_schema, todos_schema
from ..util import validate_request


class TodoListResource(Resource):

    @validate_request
    def post(self):
        payload = request.get_json()
        try:
            todo_schema.load(payload)
        except ValidationError as err:
            return err.messages, 400

        todo = Todo(title=payload["title"])
        todo.save()
        return {"message": "todo created", "todo": todo_schema.dump(todo)}, 201
    
    
    def get(self):
        todos = Todo.query.all()
        todos_schema.dump(todos)
        return {"message": "todos retrieved", "todos": todos_schema.dump(todos)}, 200



class TodoResource(Resource):

    def get(self, todo_id):
        todo = Todo.query.get(todo_id)
        if not todo:
            return {"message": f"todo with id {todo_id} does not exist"}, 404
        else:
             return {"message": "todo retrieved", "todo": todo_schema.dump(todo)}, 200
    
    def delete(self, todo_id):
        todo = Todo.query.get(todo_id)
        if not todo:
            return {"message": f"todo with id {todo_id} does not exist"}, 404
        else:
            todo.delete()
            return {"message": "todo deleted"} , 200
    
    @validate_request
    def put(self, todo_id):
        payload = request.get_json()
        todo = Todo.query.get(todo_id)
        if not todo:
            return {"message": f"todo with id {todo_id} does not exist"}, 404
        try:
            todo_schema.load(payload)
        except ValidationError as err:
            return err.messages, 400
        todo.title = payload["title"]
        todo.save()
        return {"message": "todo updated", "todo": todo_schema.dump(todo)}, 200
            