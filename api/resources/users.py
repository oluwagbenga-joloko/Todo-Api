import jwt

from flask_restful import Resource
from datetime import datetime, timedelta
from flask import request, jsonify, current_app
from marshmallow import ValidationError
from ..models import User, user_schema, user_login_schema
from ..util import validate_request, generate_token


class UserListResource(Resource):

    @validate_request
    def post(self):
        payload = request.get_json()
        try:
            data = user_schema.load(payload)
        except ValidationError as err:
            return {"message": "validation failed", "errors": err.messages}, 422

        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user: 
            return {"message": "user with email already exists"}, 400

        user = User(**data)
        user.save()
        token = generate_token(user)

        return {"message": "user created", "token": token}, 201

class AuthResource(Resource):

    @validate_request
    def post(self):
        payload = request.get_json()
        try:
             data = user_login_schema.load(payload)
        except ValidationError as err:
             return {"message": "validation failed", "errors": err.messages}, 422
        user = User.query.filter_by(email=data["email"]).first()
        if user:
            if user.verify_password(data["password"]):
                token = generate_token(user)
                return {"message": "log in successfull", "token": token}, 200

        return {"message" : "invalid email or password"}, 401

        



# class TodoResource(Resource):

#     def get(self, todo_id):
#         todo = Todo.query.get(todo_id)
#         if not todo:
#             return {"message": f"todo with id {todo_id} does not exist"}, 404
#         else:
#              return {"message": "todo retrieved", "todo": todo_schema.dump(todo)}, 200
    
#     def delete(self, todo_id):
#         todo = Todo.query.get(todo_id)
#         if not todo:
#             return {"message": f"todo with id {todo_id} does not exist"}, 404
#         else:
#             todo.delete()
#             return {"message": "todo deleted"} , 200
    
#     @validate_request
#     def put(self, todo_id):
#         payload = request.get_json()
#         todo = Todo.query.get(todo_id)
#         if not todo:
#             return {"message": f"todo with id {todo_id} does not exist"}, 404
#         try:
#             todo_schema.load(payload)
#         except ValidationError as err:
#             return err.messages, 400
#         todo.title = payload["title"]
#         todo.save()
#         return {"message": "todo updated", "todo": todo_schema.dump(todo)}, 200
            




