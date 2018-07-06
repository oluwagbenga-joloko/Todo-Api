from flask_restful import Resource
from flask import request, jsonify, make_response
from ..models import db , Todo

class TodoList(Resource):
    def post(self):
        payload = request.get_json()
        todo = Todo(title=payload["title"])
        todo.save()
        response = jsonify({"message": "todo created", "todo": todo.serialize()})
        response.status_code = 201
        return response
    



