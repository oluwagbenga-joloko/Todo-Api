import jwt

from flask_restful import Resource
from datetime import datetime, timedelta
from flask import request, jsonify, current_app, g
from marshmallow import ValidationError
from ..models import User, user_schema, user_login_schema, user_update_schema
from ..util import validate_request, generate_token, jwt_required, limiter


class UserListResource(Resource):

    decorators = [limiter.limit('10 per minute')]
    
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

        return {"message": "user created", "token": token, "user": user_schema.dump(user)}, 201

class UserResource(Resource):

    @validate_request
    @jwt_required
    def put(self, user_id):
        payload = request.get_json()
        user = User.query.get(user_id)

        if not user:
            return {"message": "user does not exist"}, 404

        if user.id != g.current_user["id"]:
            return {"message": "unauthorized"}, 401
        try:
            data = user_update_schema.load(payload)
        except ValidationError as err:
            return {"message": "validation failed", "errors": err.messages}, 422
        
        if "email" in data:
            existing_user = User.query.filter_by(email=data["email"]).first()
            if existing_user: 
                return {"message": "user with email already exists"}, 409

        for value in data:
            setattr(user, value, data[value])
        user.save()
    
        return {"message": "user updated", "user": user_schema.dump(user)}, 200


class AuthResource(Resource):

    decorators = [limiter.limit('10 per minute')]

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




