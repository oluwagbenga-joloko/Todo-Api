from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

db = SQLAlchemy()


class ModelOpsMixin():

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement='auto')

    def serialize(self):
        return { column_name: getattr(self, column_name) for column_name in self.__mapper__.c.keys() }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()

    def delete():
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()


class Todo(ModelOpsMixin, db.Model):
    title = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.title
