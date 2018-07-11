from flask import  request, current_app, g
from functools import wraps
from datetime import datetime, timedelta
import jwt


def validate_request(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.get_json():
            return {"message": "request must be a valid JSON"}, 400
        return f(*args, **kwargs)
    return decorated



def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header: 
            return {"message": "no authorization token provided"}, 400
        
        if auth_header.split(' ')[0].lower() != "bearer":
            return {"message": "invalid Authorization header, authorization header should begin with Bearer"}, 400
        
        auth_token = auth_header.split(' ')[1]
        secret = current_app.config.get("SECRET_KEY")

        try:
            decoded = jwt.decode(auth_token, secret, algorithm='HS256')
        except jwt.ExpiredSignatureError:
            return {"message": "authorization token has expired"}, 401
        except jwt.InvalidTokenError:
            return {"message": "authoriation token is invalid"}, 401

        g.current_user = decoded["user"]   
        return f(*args, **kwargs)
    return decorated


def generate_token(user):
    token  = jwt.encode({"user": {"id": user.id, "email": user.email },
                         "exp": datetime.utcnow() + timedelta(hours=24)},
                          current_app.config.get("SECRET_KEY"), algorithm='HS256')
    return token.decode()

