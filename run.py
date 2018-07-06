import os
from api.main import create_flask_app

app = create_flask_app(os.getenv('ENVIRONMENT'))

if __name__ == "__main__":
    app.run()

