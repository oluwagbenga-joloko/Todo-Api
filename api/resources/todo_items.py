from flask_restful import Resource
from flask import request, jsonify, g
from marshmallow import ValidationError
from ..models import ( Todo , todo_schema, todos_schema, 
                       TodoItem, todo_item_schema, todo_item_update_schema)
from ..util import validate_request, jwt_required


class TodoItemListResource(Resource):

    @validate_request
    @jwt_required
    def post(self, todo_id):
        payload = request.get_json()
        todo = Todo.query.get(todo_id)
        user_id = g.current_user["id"]
        if not todo:
            return {"message": "todo does not exist"}, 404 
        if todo.user_id != user_id:
            return {"message": "unauthorized"}, 401
        try:
            todo_item_schema.load(payload)
        except ValidationError as err:
            return {"message": "validation failed", "errors": err.messages}, 422

        todo_item = TodoItem(content=payload["content"], todo_id=todo.id)
        todo_item.save()
        return {"message": "todo item created", "todo_item": todo_item_schema.dump(todo_item)}, 201


class TodoItemResource(Resource):
    
    @jwt_required
    def delete(self, todo_id, todo_item_id):
        user_id = g.current_user["id"]
        todo = Todo.query.get(todo_id)
        if not todo:
            return {"message": "todo does not exist"}, 404

        if todo.user_id != user_id:
            return {"message": "unauthorized"}, 401
        
        todo_item = TodoItem.query.filter_by(id=todo_item_id, todo_id=todo_id).first()

        if not todo_item:
             return {"message": "todo item does not exist"}, 404


        todo_item.delete()
        return {"message": "todo item deleted"} , 200
    
    @validate_request
    @jwt_required
    def put(self, todo_id, todo_item_id):
        payload = request.get_json()
        user_id = g.current_user["id"]
        todo = Todo.query.get(todo_id)
        if not todo:
            return {"message": "todo does not exist"}, 404

        if todo.user_id != user_id:
            return {"message": "unauthorized"}, 401  
        
        todo_item = TodoItem.query.filter_by(id=todo_item_id, todo_id=todo_id).first()

        if not todo_item:
             return {"message": "todo item does not exist"}, 404

        try:
            data = todo_item_update_schema.load(payload)
        except ValidationError as err:
            return {"message": "validation failed", "errors": err.messages}, 422
        
        for value in data:
            setattr(todo_item, value, data[value])
    
        todo_item.save()
        return {"message": "todo_item updated", "todo_item": todo_item_schema.dump(todo_item)}, 200
            