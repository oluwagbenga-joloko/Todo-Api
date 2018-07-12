from flask_sqlalchemy import SQLAlchemy
import bcrypt
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property
from marshmallow import Schema, fields, ValidationError

db = SQLAlchemy()


class ModelOpsMixin(db.Model):

    __abstract__= True

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement='auto')
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def serialize(self):
        return { column_name: getattr(self, column_name) for column_name in self.__mapper__.c.keys() }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise SQLAlchemyError

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise SQLAlchemyError


class Todo(ModelOpsMixin):

    title = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('todos', lazy=True))

    def __repr__(self):
        return '<User %r>' % self.title

class TodoItem(ModelOpsMixin):
    content = db.Column(db.String(), nullable=False)
    complete = db.Column(db.Boolean, nullable=False, default=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)
    todo = db.relationship('Todo', backref=db.backref('todo_item'))


class User(ModelOpsMixin):
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    hash_password = db.Column(db.String(), nullable=False)

    @property
    def password(self):
        return self.hash_password
    
    @password.setter
    def password(self , value):
        self.hash_password = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
    
    def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.hash_password.encode())
    


# ### schemas #####


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')
def validate_password(data):
    if not data:
        raise ValidationError('Data not provided.')
    if len(data) < 5:
        raise ValidationError('Password must be longer than 5 characters')



class SchemaOpsMixin(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class TodoSchema(SchemaOpsMixin):

    title = fields.String(required=True, validate=must_not_be_blank)
    user_id = fields.Integer(dump_only=True)

class TodoItemSchema(SchemaOpsMixin):
    content = fields.String(required=True, validate=must_not_be_blank)
    complete = fields.Boolean()
    todo_id = fields.Integer(dump_only=True)


class UserSchema(SchemaOpsMixin):
    first_name=fields.String(required=True, validate=must_not_be_blank)
    last_name=fields.String(required=True, validate=must_not_be_blank)
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate_password, load_only=True)




user_schema = UserSchema()
user_login_schema = UserSchema(only=("email", "password"))
user_update_schema = UserSchema(partial=True)

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

todo_item_schema = TodoItemSchema()
todo_item_update_schema = TodoItemSchema(partial=True)




