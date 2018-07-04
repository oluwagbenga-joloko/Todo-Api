from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement='auto')
    title = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.title
